import concurrent.futures
import time


def main(tickers,name_of_method):
  
  
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = [executor.submit(name_of_method, sy) for sy in tickers]
  
  for f in concurrent.futures.as_completed(results):
    f.result()

def call_me(tickers,name_of_method):
    while 1:
        try:
            
            main(tickers, name_of_method)
        
            print("sleeping a while... ")
            time.sleep(10)
        except KeyboardInterrupt as e:
            print("ok .. ending")
        except Exception as f:
            print(f)
            pass
        
