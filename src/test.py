from tag.alphabet import number

print(number)

cat = {"A", "B", "A", "C", "A", "C", "A", "C"}
cow = {"A" : "cat", "B": "dog", "C":"bat", "D" : None}

print(cat)
print(cow.get("D", "fish"))
print(chr(0))

cat = None
bird = cat or "fish"
dog = bird.join(bird)
print(cat)
print(bird)
print(dog)