import os
import subprocess
import importlib.util
import folder_paths
import shutil
import sys
import traceback

from  .efficiency_nodes import NODE_CLASS_MAPPINGS
from  .py.ttl_nn_latent_upscaler import NNLatentUpscale
from  .py.city96_latent_upscaler import LatentUpscaler

NODE_CLASS_MAPPINGS = {
    "KSampler (Efficient)": TSC_KSampler,
    "KSampler Adv. (Efficient)":TSC_KSamplerAdvanced,
    "KSampler SDXL (Eff.)": TSC_KSamplerSDXL,
    "Efficient Loader": TSC_EfficientLoader,
    "Eff. Loader SDXL": TSC_EfficientLoaderSDXL,
    "LoRA Stacker": TSC_LoRA_Stacker,
    "Control Net Stacker": TSC_Control_Net_Stacker,
    "Apply ControlNet Stack": TSC_Apply_ControlNet_Stack,
    "Unpack SDXL Tuple": TSC_Unpack_SDXL_Tuple,
    "Pack SDXL Tuple": TSC_Pack_SDXL_Tuple,
    "XY Plot": TSC_XYplot,
    "XY Input: Seeds++ Batch": TSC_XYplot_SeedsBatch,
    "XY Input: Add/Return Noise": TSC_XYplot_AddReturnNoise,
    "XY Input: Steps": TSC_XYplot_Steps,
    "XY Input: CFG Scale": TSC_XYplot_CFG,
    "XY Input: Sampler/Scheduler": TSC_XYplot_Sampler_Scheduler,
    "XY Input: Denoise": TSC_XYplot_Denoise,
    "XY Input: VAE": TSC_XYplot_VAE,
    "XY Input: Prompt S/R": TSC_XYplot_PromptSR,
    "XY Input: Aesthetic Score": TSC_XYplot_AScore,
    "XY Input: Refiner On/Off": TSC_XYplot_Refiner_OnOff,
    "XY Input: Checkpoint": TSC_XYplot_Checkpoint,
    "XY Input: Clip Skip": TSC_XYplot_ClipSkip,
    "XY Input: LoRA": TSC_XYplot_LoRA,
    "XY Input: LoRA Plot": TSC_XYplot_LoRA_Plot,
    "XY Input: LoRA Stacks": TSC_XYplot_LoRA_Stacks,
    "XY Input: Control Net": TSC_XYplot_Control_Net,
    "XY Input: Control Net Plot": TSC_XYplot_Control_Net_Plot,
    "XY Input: Manual XY Entry": TSC_XYplot_Manual_XY_Entry,
    "Manual XY Entry Info": TSC_XYplot_Manual_XY_Entry_Info,
    "Join XY Inputs of Same Type": TSC_XYplot_JoinInputs,
    "Image Overlay": TSC_ImageOverlay,
    "Noise Control Script": TSC_Noise_Control_Script,
    "HighRes-Fix Script": TSC_HighRes_Fix,
    "Tiled Upscaler Script": TSC_Tiled_Upscaler,
    "Evaluate Integers": TSC_EvaluateInts,
    "Evaluate Floats": TSC_EvaluateFloats,
    "Evaluate Strings": TSC_EvaluateStrs,
     "Simple Eval Examples": TSC_EvalExamples,
     "NNLatentUpscale" : NNLatentUpscale,
     "LatentUpscaler" : LatentUpscaler
}
NODE_DISPLAY_NAME_MAPPINGS = {
     "KSampler (Efficient)": "EFF_KSampler",
     "KSampler Adv. (Efficient)":"EFF_KSamplerAdvanced",
     "KSampler SDXL (Eff.)": "EFF_KSamplerSDXL",
     "Efficient Loader": "EFF_EfficientLoader",
     "Eff. Loader SDXL": "EFF_EfficientLoaderSDXL",
     "LoRA Stacker": "EFF_LoRA_Stacker",
     "Control Net Stacker": "EFF_Control_Net_Stacker",
     "Apply ControlNet Stack": "EFF_Apply_ControlNet_Stack",
     "Unpack SDXL Tuple": "EFF_Unpack_SDXL_Tuple",
     "Pack SDXL Tuple": "EFF_Pack_SDXL_Tuple",
     "XY Plot": "EFF_XYplot",
     "XY Input: Seeds++ Batch": "EFF_XYplot_SeedsBatch",
     "XY Input: Add/Return Noise": "EFF_XYplot_AddReturnNoise",
     "XY Input: Steps": "EFF_XYplot_Steps",
     "XY Input: CFG Scale": "EFF_XYplot_CFG",
     "XY Input: Sampler/Scheduler": "EFF_XYplot_Sampler_Scheduler",
     "XY Input: Denoise": "EFF_XYplot_Denoise",
     "XY Input: VAE": "EFF_XYplot_VAE",
     "XY Input: Prompt S/R": "EFF_XYplot_PromptSR",
     "XY Input: Aesthetic Score": "EFF_XYplot_AScore",
     "XY Input: Refiner On/Off": "EFF_XYplot_Refiner_OnOff",
     "XY Input: Checkpoint": "EFF_XYplot_Checkpoint",
     "XY Input: Clip Skip": "EFF_XYplot_ClipSkip",
     "XY Input: LoRA": "EFF_XYplot_LoRA",
     "XY Input: LoRA Plot": "EFF_XYplot_LoRA_Plot",
     "XY Input: LoRA Stacks": "EFF_XYplot_LoRA_Stacks",
     "XY Input: Control Net": "EFF_XYplot_Control_Net",
     "XY Input: Control Net Plot": "EFF_XYplot_Control_Net_Plot",
     "XY Input: Manual XY Entry": "EFF_XYplot_Manual_XY_Entry",
      "Manual XY Entry Info": "EFF_XYplot_Manual_XY_Entry_Info",
      "Join XY Inputs of Same Type": "EFF_XYplot_JoinInputs",
      "Image Overlay": "EFF_ImageOverlay",
      "Noise Control Script": "EFF_Noise_Control_Script",
      "HighRes-Fix Script": "EFF_HighRes_Fix",
      "Tiled Upscaler Script": "EFF_Tiled_Upscaler",
      "Evaluate Integers": "EFF_EvaluateInts",
      "Evaluate Floats": "EFF_EvaluateFloats",
      "Evaluate Strings": "EFF_EvaluateStrs",
      "Simple Eval Examples": "EFF_EvalExamples",
      "NNLatentUpscale" : "EFF_NNLatentUpscale",
      "LatentUpscaler" : "EFF_LatentUpscaler"
}
WEB_DIRECTORY = "js"

CC_VERSION = 2.0

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'CC_VERSION']
