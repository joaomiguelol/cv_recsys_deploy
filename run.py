import logging
from omegaconf import DictConfig, OmegaConf

import hydra


logger = logging.getLogger(__name__)


def train(cfg):
    logger.info(OmegaConf.to_yaml(OmegaConf.to_container(cfg, resolve=True)))

    logger.info("Training complete.")

@hydra.main(config_path="configs", config_name="config")
def main(cfg: DictConfig) -> None:
    train(cfg)

if __name__ == "__main__":
    main()

# EOF
