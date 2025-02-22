def calculate_love_score(name1, name2):
    t = 0
    l = 0
    for a in (name1+name2).lower():
      if a in "true":
          t= t+1
      if a in "love":
          l= l+1
    print(f"{t}{l}")

 
# Call your function with hard coded values
calculate_love_score("Kanye West", "Kim Kardashian")