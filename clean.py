#!/c/Python38/python

from pathlib import Path

if __name__ == '__main__':

  try:
    for p in Path('.').glob('scrapped-links-*.txt'):
      p.unlink()
  except: pass
  
  try:
    for p in Path('.').glob('to-scrap-*.txt'):
      p.unlink()
  except: pass
  
  try:
    Path('./debug.log').unlink()
  except: pass

  try:
    Path('./sitemap.xml').unlink()
  except: pass
