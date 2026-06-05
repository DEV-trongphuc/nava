with open("sapo_BWT_using_no_change_it/Templates/collection.bwt", "r", encoding="utf-8") as f:
    content = f.read()

with open("scratch/original_collection.bwt", "w", encoding="utf-8") as out:
    out.write(content)
print("Done!")
