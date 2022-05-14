### Installation
```pip install fivesimapi```

### Example Code
```python
import FiveSimApi, asyncio
from FiveSimApi import fivesim

async def main():
    five_sim = fivesim.FiveSim(api_key)
    data = await sm.get_profile()
    print(data)

asyncio.run(main())
```
