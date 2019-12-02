import urllib.request
#import ssl

def main():
    request = input('请输入网址，以http或https开头，以"/"结尾：')
    while(1):
        try:
            local = input('请输入保存地址，默认为D盘根目录（斜杠请用"\\"）：')  #保存地址，地址中的反斜杠'\'前需要再加一个反斜杠
        except FileNotFoundError:
            print("地址不存在，请确认后重新输入。")
        else:
            if local == '':
                local = "D:\\"
            break

    page = urllib.request.urlopen(request)
    html = page.read().decode()
    html_splited = html.split('\n')
    def find_img(st):
        #传入一行，查找其中是否有以"jpg"或"png"结尾的文件，返回为所有符合条件的文件地址（字符串列表）或空列表（没找到）
        address = []
        splited = st.split('"') #用双引号'"'切割
        for i_st in splited:
            if (i_st.endswith('.jpg') or i_st.endswith('.png')):   #如果以jpg或png结尾
                if not i_st.startswith('http'): #如果以http开头则不做处理，否则添加当前网页的地址
                    i_st = request + i_st
                address.append(i_st)
        return address

    def download_img(st):   #输入图片地址，下载图片并保存在本地的local位置，文件名为原文件名
        name = st[st.rfind('/')+1:]
        local_address = local + '/' + name
        try:    #理想状态直接可以运行
            print("Trying to download: %s." % name)
            urllib.request.urlretrieve(st,local_address)
            print("Successfully downloaded.")
        except AttributeError:  #解决不知道为什么会产生但是重新手动加一个http就能好的bug
            if st.startswith('https'):
                st_change = r'https://'+st.split(r'://',1)[1]
            else:
                st_change = r'http://' + st.split(r'://',1)[1]
            try:    #如果仍然报错
                print("Trying to download: %s." % name)
                urllib.request.urlretrieve(st_change,local_address)
                print("Successfully downloaded." % name)
            except AttributeError:
                print('出现错误，程序终止。请关闭程序后找到原py文件，打开后（可以用记事本）删除第二行开头的井号#。')
                exit()

    for i in html_splited:  #对html里的每一行
        list = find_img(i)   #获取可能的文件列表
        for string in list:     #尝试下载每个文件
            download_img(string)

    print('Finished.')

if __name__ == '__main__':
    main()
