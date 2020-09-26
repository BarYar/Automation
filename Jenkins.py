def fibonacci(n):
    num1=0
    num2=1
    for i in range(n):
        print(num1)
        sum = num1 + num2
        num1=num2
        num2=sum
import urllib.request, json
with urllib.request.urlopen("https://www.random.org/integers/?num=1&min=1&max=100&col=1&base=10&format=plain&rnd=new") as url:
    data = json.loads(url.read().decode())
    print(data)
fibonacci(data)

