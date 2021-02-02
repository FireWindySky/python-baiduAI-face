import requests,base64,pygame,sys
from time import sleep
from pygame.locals import *

image="test.jpg"


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def face_test(face_image_path):
    f = get_file_content(face_image_path)
    data = base64.b64encode(f) 
    return data,data.decode()

try:
    dface,ff=face_test(image)
except:
    print("图片读取发生错误")
    exit()
access_token='your baidu access_token'


request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
request_url = request_url + "?access_token=" + access_token
params={
    'image':str(dface,'utf-8'),
    'image_type':'BASE64',
    'face_field':'beauty,age,expression,face_shape,gender,glasses,emotion,eye_status,face_type,mask'
}
headers = {'content-type': 'application/json'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    r=response.json()['result']['face_list'][0]

beauty_s=r['beauty']
age_s=r['age']
face_shape=r['face_shape']['type']
expression=r['expression']['type']
gender=r['gender']['type']
emotion=r['emotion']['type']
glasses=r['glasses']['type']
eye_left=r['eye_status']['left_eye']
eye_right=r['eye_status']['right_eye']
face_type=r['face_type']['type']
mask=r['mask']['type']

d_gender={"male":"男性", "female":"女性"}
d_expression={"none":"不笑","smile":"微笑","laugh":"大笑"}
d_face_shape={"square":"正方形", "triangle":"三角形", "oval":"椭圆", "heart":"心形", "round":"圆形"}
d_emotion={"angry":"愤怒", "disgust":"厌恶", "fear":"恐惧", "happy":"高兴", "sad":"伤心", "surprise":"惊讶", "neutral":"无表情", "pouty":"撅嘴", "grimace":"鬼脸"}
d_glasses={"none":"无眼镜","common":"普通眼镜","sun":"墨镜"}
d_face_type={"human": "真实人脸", "cartoon": "卡通人脸"}
d_mask={0:'无口罩',1:"戴口罩"}

gender=d_gender[gender]
expression=d_expression[expression]
emotion=d_emotion[emotion]
face_shape=d_face_shape[face_shape]
glasses=d_glasses[glasses]
face_type=d_face_type[face_type]
mask=d_mask[mask]
if eye_left>0.5:
    eye_left="睁开"
else:
    eye_left="闭合"
if eye_right>0.5:
    eye_right="睁开"
else:
    eye_right="闭合"

p="最终评价:你"
if beauty_s<50:
    p+="是真的丑！"
elif beauty_s<60 :
    p+="比较丑"
elif beauty_s<=70:
    p+="还凑合"
elif beauty_s<82:
    p+="挺好看的"
else:
    p+="实在是太漂亮啦！"

pygame.init()
pygame.display.set_caption("颜值评分小程序")
bg_size=width,height=1280,720
screen=pygame.display.set_mode(bg_size)
img=pygame.image.load(image)
rect=img.get_rect()
heng=rect.right-rect.left
zong=rect.bottom-rect.top

if heng >= 3000 or zong >= 3000:
    img = pygame.transform.scale(img, (int(heng /8), int(zong /8)))
elif heng >= 1000 or zong >= 1000:
    img = pygame.transform.scale(img, (int(heng / 4), int(zong / 4)))
elif heng>=800 or zong>=620:
    img=pygame.transform.scale(img, (int(heng/2),int(zong/2)))

fclock=pygame.time.Clock()
rect=img.get_rect()

rect=rect.move(590, 50)
speed=5
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    screen.fill((255, 255, 255))
    screen.blit(img, rect)

    if rect.bottom>720 and speed==5:
        speed=-5
    elif rect.top<0 and speed==-5:
        speed = 5
    rect = rect.move(0, speed)
        font = pygame.font.Font("C:\\Windows\\Fonts\\msyh.ttc", 30)
    font1 = pygame.font.Font("C:\\Windows\\Fonts\\STXINGKA.TTF", 50)

    text = font.render("你的年龄约为"+str(age_s)+"岁, 性别:"+str(gender), 1, (10, 10, 10))
    text1 = font.render("笑容:"+expression+", 情绪:"+emotion, 1, (10, 10, 10))
    text2 = font.render("脸型:"+face_shape+", 眼镜:"+glasses, 1, (10, 10, 10))
    text3 = font.render("左眼:"+eye_left+", 右眼:"+eye_right, 1, (10, 10, 10))
    text4 = font.render("人脸类型:"+face_type+", "+mask, 1, (10, 10, 10))
    text5 = font.render("颜值打分:"+str(beauty_s)+"(满分100)", 1, (10, 10, 10))
    text6 = font1.render(p, 1, (10, 10, 10))
    screen.blit(text,(20,20))

    screen.blit(text1, (20, 70))

    screen.blit(text2, (20, 120))

    screen.blit(text3, (20, 170))

    screen.blit(text4, (20, 220))

    screen.blit(text5, (20, 270))

    screen.blit(text6, (20, 330))

    pygame.display.update()
    fclock.tick(60)










