from fastapi import APIRouter, UploadFile
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

router = APIRouter()

processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

@router.post("/ocr")
async def extract_text(file: UploadFile):
    image = Image.open(file.file).convert("RGB")
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return {"text": text}
