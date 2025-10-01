import json, sys
from core.src.detector import Rulepack, decide

def main():
    try:
        with open("rulepack.json","r",encoding="utf-8") as f:
            rp = Rulepack(**json.load(f))
    except Exception:
         rp = Rulepack.default()
    #Below exists to test exeption.json
    except Exception:
        print("An error occurred. Exiting.")
        sys.exit()

    text = " ".join(sys.argv[1:]) or "FREE gift click http://bit.ly/now to claim"
    print(decide(text, rp))

if __name__ == "__main__":
    main()