import os
from litellm import completion, embedding

os.environ["NVIDIA_API_KEY"] = "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"

try:
    print("Testing completion with nvidia_nim/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning")
    response = completion(
        model="nvidia_nim/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
        messages=[{"role": "user", "content": "Hello"}],
    )
    print("Success:", response.choices[0].message.content)
except Exception as e:
    print("Error:", e)

try:
    print("Testing completion with nvidia/nemotron-3-nano-omni-30b-a3b-reasoning")
    response = completion(
        model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
        messages=[{"role": "user", "content": "Hello"}],
    )
    print("Success:", response.choices[0].message.content)
except Exception as e:
    print("Error:", e)
