from pyxform import xls2json, builder
import os
import json
from typing import Tuple, Optional
import tempfile
from uuid import uuid4

class XLSFormService:
    
    @staticmethod
    def convert_xlsform_to_xform(xlsform_data: bytes, form_id: str) -> Tuple[str, Optional[str]]:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_xls:
                temp_xls.write(xlsform_data)
                temp_xls_path = temp_xls.name
            
            try:
                json_survey = xls2json.parse_file_to_json(temp_xls_path)
                
                survey = builder.create_survey_element_from_dict(json_survey)
                
                xml_content = survey.to_xml()
                
                return xml_content, None
                
            finally:
                if os.path.exists(temp_xls_path):
                    os.remove(temp_xls_path)
                    
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def validate_xlsform(xlsform_data: bytes) -> Tuple[bool, Optional[str]]:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_xls:
                temp_xls.write(xlsform_data)
                temp_xls_path = temp_xls.name
            
            try:
                json_survey = xls2json.parse_file_to_json(temp_xls_path)
                
                if not json_survey.get('name'):
                    return False, "Form must have a name"
                
                if not json_survey.get('children'):
                    return False, "Form must have at least one question"
                
                return True, None
                
            finally:
                if os.path.exists(temp_xls_path):
                    os.remove(temp_xls_path)
                    
        except Exception as e:
            return False, str(e)

xlsform_service = XLSFormService()