# BossMatchJobHunter
Boss直聘批量投递脚本，提高找工作效率。

## 描述 
Boss直聘批量投递脚本，Boss没有批量沟通功能，而且Boss回复率太低 ，为了提高找工作效率而制作，将就能用  
~~所以这是自用的，我不会展示图片的，只用文字的描述，这样懂我的人自然会懂，不懂的就自然会放弃~~  
![Watchers](https://img.shields.io/github/watchers/20241204/BossMatchJobHunter) ![Stars](https://img.shields.io/github/stars/20241204/BossMatchJobHunter) ![Forks](https://img.shields.io/github/forks/20241204/BossMatchJobHunter) ![Vistors](https://visitor-badge.laobi.icu/badge?page_id=20241204.BossMatchJobHunter) ![LICENSE](https://img.shields.io/badge/license-CC%20BY--SA%204.0-green.svg)
<a href="https://star-history.com/#20241204/BossMatchJobHunter&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=20241204/BossMatchJobHunter&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=20241204/BossMatchJobHunter&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=20241204/BossMatchJobHunter&type=Date" />
  </picture>
</a>

## 依赖
  Python 程序  
  Edge 浏览器  
  Edge webdriver：https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/  

## 实现思路
### 首次执行脚本，判断 cookie 文件是否存在  
  不存在 cookie 文件，则先访问登录页面，给用户70秒时间让他们登陆，等时间一到，获取当前页面 cookie 并存储到当前路径中  
  然后继续给用户 300 秒的时间，通过浏览器安装插件提取浏览器可以使用的cookie  
### 再次执行脚本，判断 cookie 文件是否存在  
  存在 cookie 文件，则访问预先配置好的搜索链接 search_url 访问，并获取元素节点执行点击操作  

## 注意
  Edge webdriver 和 Edge 浏览器版本要统一，浏览器地址栏输入 edge://version/ 可以查看浏览器版本  
  
  执行脚本首先会给用户 70秒（这个可以自己修改时间）的时间登录并获取脚本所需的 cookie 文件   
  
  获取脚本 cookie 文件后会再给用户 300秒（这个可以自己修改时间），是为了让用户通过 Edge 浏览器安装 J2TEAM Cookies 插件，并提取浏览器可以使用的 cookie 提取浏览器通用 cookie 文件这样做的目的是为了让本机浏览器的 cookie 互通防止登录之后顶掉其他浏览器的登录状态，之后在其他浏览器访问 boss直聘 链接通过 J2TEAM Cookies 插件倒入浏览器通用 cookie 文件，就登录成功了  
  
  搜索链接 search_url 怎么配置，其实很简单，随便打开浏览器登录 Boss 直聘，搜索自己想要投递的职位并选择过滤条件，最后复制地址栏的地址粘贴到 Boss批量投递脚本.py 脚本的变量 search_url 中即可  

  xpath 路径官方随时会更改导致本脚本失效，你需要借助浏览器开发者工具对特定元素路径进行更新
  
## 风险(不良反应-_-)

  1、风险就是有可能会被BOSS直聘暂停访问PC端web页面，但是手机客户端不受影响，说明 B/S 框架产品和 C/S 框架产品调用的API互不影响  
  2、也许可以尝试自动化 C/S 框架产品投递简历，目前还没有思路，可能要学一些知识才能实现了，目前暂时没时间，等找到工作稳定下来再尝试  
  ![image](assets/00.jpeg)
  ![image](assets/01.jpeg)



