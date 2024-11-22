import sys
from argparse import ArgumentParser
import numpy as np
import click

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--sort', '-s', is_flag=True)
def main(path, sort):
    print(f"main called with {path}")

if __name__ == "__main__":
    main()