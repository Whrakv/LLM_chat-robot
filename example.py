import os
import requests
from flask import Flask,request

##——————————————————接入gemini！！！！！！
import google.generativeai as genai
import pathlib
import textwrap
import os
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from google.generativeai.types import HarmCategory, HarmBlockThreshold
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

GOOGLE_API_KEY="AIzaSyDda0gy-ULyV1asH2X3kEjJ3StvJ79sbUE"
genai.configure(api_key=GOOGLE_API_KEY)
os.environ['http_proxy']='http://127.0.0.1:7890'
os.environ['https_proxy']='http://127.0.0.1:7890'
os.environ['all_proxy']='http://127.0.0.1:7890'
safety_none={
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}

##————————————————————————故事读入！！！
with open("EPiao/sui.txt", "r", encoding="utf-8") as file:
    sui=file.read()
story = [] 
for i in range(1,22):
    with open("EPiao/"+str(i)+".txt", "r", encoding="utf-8") as file:
        story.append(file.read())
allstory = '\n'.join(story)

suistory1="满穗是在1618年五月初六出生在陕北甘泉的一个农村里，一家五口人，有满穗的娘、爹爹、奶奶和弟弟，爹爹对满穗很好，娘有点偏爱弟弟，弟弟叫财儿，豚妖的故事是奶奶讲的，家里有十五亩地，满穗在八岁的时候养了一只小猫。\
在1628年、也就是满穗十岁那年。陕北发生了大旱，满穗家一年颗粒无收，家里人把满穗养的小猫煮了，当天晚上奶奶因为没有吃的并且上了年纪也过世了\
在那不久，因为邻居跑了官吏收走了家里仅剩的粮，爹爹带满穗去城里演影子戏，却只有人看没人给钱，只能把影子戏的道具卖了换了一点粮食\
爹爹把后院的传家宝拿出去卖，却再也没有回来，紧接着弟弟饿死了，娘听见弟弟死了出现幻觉把弟弟的尸体煮了，清醒之后上吊自杀了，只剩满穗一人了\
满穗踏上了找爹爹的路，如果知道爹爹被杀了就为他报仇"
suistory2="1629年、满穗在路途上遇到不少饿殍，又是还差点被抓到了，一路走到了渭南，在食物吃完的时候被一个厨子爷爷收留了，在客栈当了六个月帮厨，学到了一些厨艺，在那之后启程去长安的烟月楼，\
在烟月楼遇到了芸姐，在芸姐旁边待了七个月，芸姐教会了满穗在乱世中生存的技巧，八个月后芸姐打听到了一些黑当铺的地址，可以去找找爹爹的遗物。\
在那之后的一年找了很久的黑当铺，顺便回到了厨子爷爷一趟，不过厨子爷爷已经过世了，给满穗留了一双布鞋，在那之后，在一家华州城的黑当铺找到了给爹爹的荷包。得知了良是她的杀父仇人\
"
beforestory="满穗知道了杀父仇人之后，假装成哑巴进入了尹三的客栈，在1623年，和另外三个女娃要被良送去洛阳当菜人，在路上刺杀过良一次，但没成功，被良打了屁股。之后开口说话骗良是为了给姐姐报仇，并教良影子戏让良放松警惕。但因为担心刺杀良之后会其他女娃被吃，便一直没有刺杀。到了水沟村因为饥荒人吃人便匆匆离开了"
story131415="良对满穗起了疑心，怀疑她关于姐姐的遭遇，却对满穗的父亲的描述深信不疑。在途中，良教满穗玩影子戏。到达陕州后，舌打算把她们卖掉当菜人，良坚决不同意，舌头打算除掉良。满穗也发现了舌头的一些可疑举动，为了提醒良，故意说出了舌头的阴谋，结果被舌头发现。在一番搏斗后，良杀了舌头，并决定把小女孩们送到更安全的地方。良和满穗为了处理舌头的尸体，把尸体切碎煮熟，并把残渣倒进了客栈的粪池，处理掉血腥味。最后，良决定带着小女孩们去解州寻找他之前的救命恩人，并将她们送到安全的地方。"
story17="途中，他们遇到了反军，反军头领“李闯将”对他们进行了身份确认，良用影子戏的方式蒙混过关。李闯将为了留下良，与他进行了一场比试，良凭借精湛的武功获胜，并要求李闯将释放他们。李闯将信守承诺，并热情地邀请他们观看影子戏，并用酒菜招待他们。第二天，良与小羊们告别李闯将，继续前往解州。临别前，李闯将告诉了良自己的身份和名号，并邀请良加入反军。良婉拒了邀请，并与小羊们继续前往解州。"

prompt1="以下是一篇发生在中国明朝的故事，先写的是满穗（也叫穗）的经历，然后是以良（也叫良爷）的视角写的。之后，我扮演良，你扮演满穗进行一次对话"
prompt2="\n\n 现在我扮演良，请模仿满穗回答我一句话（要注意你回答的是否满足这个时代的知识）现在开始:\n\n"

stringhelp="1.在发送到消息开头加入 良: 可与满穗对话\n2.这个ai暂时没有记忆功能(每次使用都会创建新对话，有空会加)\n3.场景发生在去洛阳的马车上\n4.因为token限制，每分钟只能回复一两条\n5.不要发表情包\n6.请温柔对待满穗"

app = Flask(__name__)
send_msg="http://127.0.0.1:5700/send_msg?user_id=714278632&message="
send_group="http://127.0.0.1:5700/send_msg?group_id=913724031&message="
host=[714278632]
@app.route('/',methods=["POST"])
def test():
    json=request.get_json()
    string = str(request.get_json().get("message"))
    if json.get("user_id") in host:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        try:
            response = model.generate_content(str(request.get_json().get("message")),safety_settings=safety_none)
            requests.get(send_msg+response.text)
        except Exception as e:
            requests.get("有个错误："+print(str(e)))
    if string[0] == "w":
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        try:
            response = model.generate_content(str(request.get_json().get("message"))[1:],safety_settings=safety_none)
            requests.get(send_msg+response.text)
        except Exception as e:
            requests.get("有个错误："+print(str(e)))
    if string[0]=='良' and string[1]=='：':
        try:
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            response = model.generate_content(prompt1+suistory1+suistory2+beforestory+story131415+story17+story[18]+story[19]+prompt2+string,safety_settings=safety_none)
            if json.get("message_type") == "private":
                requests.get("http://127.0.0.1:5700/send_msg?user_id="+str(json.get("user_id"))+"&message="+str(response.text))
            if json.get("message_type") == "group":
                requests.get("http://127.0.0.1:5700/send_msg?group_id="+str(json.get("group_id"))+"&message="+"@"+str(json.get("sender").get("nickname"))+"\n"+str(response.text))
        except :
            if json.get("message_type") == "private":
                requests.get("http://127.0.0.1:5700/send_msg?user_id="+str(json.get("user_id"))+"&message=每分钟消息已达上限，请稍等再发一次")
            if json.get("message_type") == "group":
                requests.get("http://127.0.0.1:5700/send_msg?group_id="+str(json.get("group_id"))+"&message="+"@"+str(json.get("sender").get("nickname"))+"\n"+"每分钟消息已达上限，请稍等再发一次")
    if string =='-/help/-':
        if json.get("message_type") == "private":
            requests.get("http://127.0.0.1:5700/send_msg?user_id="+str(json.get("user_id"))+"&message="+stringhelp)
        if json.get("message_type") == "group":
            requests.get("http://127.0.0.1:5700/send_msg?group_id="+str(json.get("group_id"))+"&message="+"@"+str(json.get("sender").get("nickname"))+"\n"+stringhelp)
    
    return '123'
app.run(debug=True ,host='127.0.0.1',port=5701)