import pandas as pd
import logging
from typing import Dict, List, Tuple
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from datetime import datetime

from trade.models import OilBase, FuelType, Lot


logger = logging.getLogger('common')


class CSVLotsProcessingService:
    REQUIRED_COLUMNS = [
        'lot_date',
        'ksss_nb_code',
        'ksss_fuel_code',
        'initial_volume',
        'available_volume',
        'status',
        'price_per_ton'
    ]
    
    STATUS_MAP = {
        'Подтвержден': 'confirmed',
        'Продан': 'sold',
        'Неактивен': 'inactive'
    }

    DATE_FORMATS = [
        '%Y-%m-%d',
        '%d.%m.%Y',
        '%Y/%m/%d',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%d %H:%M:%S%z',
    ]

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def validate_columns(self) -> List[str]:
        return [col for col in self.REQUIRED_COLUMNS if col not in self.df.columns]

    def parse_date_safely(self, date_str) -> datetime:
        for date_format in self.DATE_FORMATS:
            try:
                parsed_date = datetime.strptime(str(date_str), date_format)
                if timezone.is_naive(parsed_date):
                    parsed_date = timezone.make_aware(parsed_date)
                return parsed_date
            except ValueError:
                continue

        logger.warning(f"Could not parse date: {date_str}, using current date instead")
        return timezone.now()

    def _prepare_reference_data(self) -> Tuple[Dict, Dict]:
        unique_oil_base_codes = self.df['ksss_nb_code'].unique()
        unique_fuel_type_codes = self.df['ksss_fuel_code'].unique()

        existing_oil_bases = {
            ob.ksss_code: ob for ob in 
            OilBase.objects.filter(ksss_code__in=unique_oil_base_codes)
        }
        existing_fuel_types = {
            ft.ksss_code: ft for ft in 
            FuelType.objects.filter(ksss_code__in=unique_fuel_type_codes)
        }

        new_oil_bases = [
            OilBase(
                ksss_code=code,
                name=f"Нефтебаза #{code}",
                region="Неизвестный регион",
                address="Не указан"
            )
            for code in unique_oil_base_codes if code not in existing_oil_bases
        ]
        created_oil_bases = OilBase.objects.bulk_create(new_oil_bases)
        for ob in created_oil_bases:
            existing_oil_bases[ob.ksss_code] = ob

        new_fuel_types = [
            FuelType(
                ksss_code=code,
                name=f"Топливо #{code}",
                description="Описание отсутствует"
            )
            for code in unique_fuel_type_codes if code not in existing_fuel_types
        ]
        created_fuel_types = FuelType.objects.bulk_create(new_fuel_types)
        for ft in created_fuel_types:
            existing_fuel_types[ft.ksss_code] = ft

        return existing_oil_bases, existing_fuel_types

    def _create_lots(self, existing_oil_bases: Dict, existing_fuel_types: Dict) -> List[Lot]:
        lots = []
        for _, row in self.df.iterrows():
            oil_base = existing_oil_bases[row['ksss_nb_code']]
            fuel_type = existing_fuel_types[row['ksss_fuel_code']]

            expiration_date = self.parse_date_safely(row['lot_date'])

            lots.append(Lot(
                expiration_date=expiration_date,
                oil_base=oil_base,
                fuel_type=fuel_type,
                initial_volume=Decimal(str(row['initial_volume'])),
                available_volume=Decimal(str(row['available_volume'])),
                status=self.STATUS_MAP.get(row['status'], 'confirmed'),
                price_per_ton=Decimal(str(row['price_per_ton']))
            ))

        return lots

    @transaction.atomic
    def process(self) -> Dict:
        logger.info("Starting CSV processing...")
        
        missing_columns = self.validate_columns()
        if missing_columns:
            return {
                "success": False,
                "error": f"Missing required columns: {', '.join(missing_columns)}"
            }

        try:
            df_cleaned = self.df.dropna()
            if len(df_cleaned) == 0:
                return {
                    "success": False,
                    "error": "No valid data rows found after filtering"
                }
            
            self.df = df_cleaned

            existing_oil_bases, existing_fuel_types = self._prepare_reference_data()
            lots = self._create_lots(existing_oil_bases, existing_fuel_types)

            created_lots = Lot.objects.bulk_create(lots)

            result = {
                "success": True,
                "created": {
                    "oil_bases": len(existing_oil_bases),
                    "fuel_types": len(existing_fuel_types),
                    "lots": len(created_lots)
                },
                "total_rows": len(self.df)
            }

            logger.info(f"CSV processing completed: {result}")
            return result

        except Exception as e:
            logger.error(f"Error during CSV processing: {str(e)}")
            return {"success": False, "error": str(e)}
