# Containers

A reproducible GPU container image is planned, but no Docker image is currently certified or tested. Until an image is validated against the target cloud provider's driver/runtime configuration, follow the environment setup in [the cloud guide](../docs/cloud.md).

Future images should pin compatible PyTorch/CUDA dependencies, run as a non-root user where practical, mount datasets and artifacts as volumes, and never bake credentials or private training data into image layers.
