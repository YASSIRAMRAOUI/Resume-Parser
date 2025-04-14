import os


def get_env(key: str) -> str:
   value = os.environ.get(key)

   if value is None:
       raise RuntimeError(f'The environment variable {key} is not set')

   return value