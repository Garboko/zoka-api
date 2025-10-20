from pyxform import xls2json, builder
import os
import json
from typing import Tuple, Optional
import tempfile
import logging

logger = logging.getLogger(__name__)

class XLSFormService:
    
    @staticmethod
    def convert_xlsform_to_xform(xlsform_data: bytes, form_id: str) -> Tuple[Optional[str], Optional[str]]:
        temp_xls_path = None
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_xls:
                temp_xls.write(xlsform_data)
                temp_xls_path = temp_xls.name
            
            logger.info(f"Converting XLSForm to XForm for form_id: {form_id}")
            
            json_survey = xls2json.parse_file_to_json(temp_xls_path)
            
            survey = builder.create_survey_element_from_dict(json_survey)
            
            xml_content = survey.to_xml()
            
            logger.info(f"XLSForm converted successfully for form_id: {form_id}")
            return xml_content, None
                
        except Exception as e:
            logger.error(f"Error converting XLSForm for form_id {form_id}: {e}", exc_info=True)
            return None, f"Conversion error: {str(e)}"
            
        finally:
            if temp_xls_path and os.path.exists(temp_xls_path):
                try:
                    os.remove(temp_xls_path)
                except Exception as e:
                    logger.warning(f"Failed to delete temp file {temp_xls_path}: {e}")
    
    @staticmethod
    def validate_xlsform(xlsform_data: bytes) -> Tuple[bool, Optional[str]]:
        temp_xls_path = None
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_xls:
                temp_xls.write(xlsform_data)
                temp_xls_path = temp_xls.name
            
            logger.info("Validating XLSForm")
            
            json_survey = xls2json.parse_file_to_json(temp_xls_path)
            
            if not json_survey.get('name'):
                logger.warning("XLSForm validation failed: missing name")
                return False, "Form must have a name"
            
            if not json_survey.get('children'):
                logger.warning("XLSForm validation failed: no questions")
                return False, "Form must have at least one question"
            
            logger.info("XLSForm validation successful")
            return True, None
                
        except Exception as e:
            logger.error(f"Error validating XLSForm: {e}", exc_info=True)
            return False, f"Validation error: {str(e)}"
            
        finally:
            if temp_xls_path and os.path.exists(temp_xls_path):
                try:
                    os.remove(temp_xls_path)
                except Exception as e:
                    logger.warning(f"Failed to delete temp file {temp_xls_path}: {e}")

xlsform_service = XLSFormService()