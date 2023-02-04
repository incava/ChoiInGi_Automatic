# 1. 엄마 떡들고 오누이가 기다리고 있는 집감
# 2. 집가는길에 호랑이만남
# 3. 떡던져줘서 호랑이 지나감
# 4. 다시만나서 떡던져주고 지나감
# 5. 다시만났는데 떡없어서 호랑이가 엄마 잡아먹음
# 6. 호랑이가 엄마인척하고 오누이 집감
# 7. 오누이 잡아먹음

isAliveOnui = True        # 오누이 생존 여부
isAliveMom = True         # 엄마 생존 여부
isMeetMomAndTiger = False # 엄마와 호랑이와 만났는지 여부
riceCake = 10             # 엄마의 남은 떡 갯수

print("엄마는 오누이가 기다리는 집에 가는 중 입니다..")
while True: 
  if isAliveMom == True: 
    isMeetMomAndTiger = True
    print("집가는 길에 호랑이를 만났습니다!")
  else:
    isMeetMomAndTiger = False
    print("엄마는 호랑이에게 잡아 먹혔습니다.")
    break

  if riceCake > 0:
    riceCake = riceCake - 1
    print("엄마는 살기위해 호랑이에게 떡을 던졌습니다.")
  else:    
    print("엄마는 더이상 남은 떡이 없습니다.")
    isAliveMom = False

for i in range(0, 3):
  print("호랑이는 오누이 집에가서 엄마인 척을 한다.")
  if i < 2:
    isAliveOnui = True
    print("오누이는 속지 않았습니다.")
  else:
    isAliveOnui = False
    print("오누이는 호랑이의 꾀에 속아 잡아 먹혔습니다.")  