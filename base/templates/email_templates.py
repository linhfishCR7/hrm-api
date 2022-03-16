from django.conf import settings

class BaseTemplate:
    BASE = """
        <!DOCTYPE html
        PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">

        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title>Demystifying Email Design</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        </head>

        </html>

        <body style="background-color: #c1c1c1; padding: 50px 0 83px 0" width="1920px" height="1339px">
            <table width="680px" cellpadding="0" cellspacing="0" style="margin-bottom: 50px; margin-right: auto; margin-left: auto;">
                <tr>
                <td align="left">
                    <img style="
                        max-width: 100%;
                        padding-top: 30px;
                        padding-left: 20px;
                        padding-right: 35px;
                    " width="172.53px" height="50px"
                    src="https://hrm-s3.s3.amazonaws.com/83849446-8b3logo-team.png" />
                </td>
                <td align="right">
                    <a href="https://www.instagram.com/linhfishcr7_it/" style="color: #fff; font-size: larger; margin-right: 15px">
                    <img
                        src="https://d1a2wccegmvxly.cloudfront.net/eyJidWNrZXQiOiAia2FybGV0LWRldi1tZWRpYSIsICJrZXkiOiAiZTlmYWNiODQtNzYyaW5zdGFncmFtLnBuZyIsICJlZGl0cyI6IHt9fQ=="
                        width="30px" height="30px" />
                    </a>
                    <a href="https://www.linkedin.com/in/linh-ha-185741215/"
                    style="color: #fff; font-size: larger; margin-right: 15px">
                    <img
                        src="https://d1a2wccegmvxly.cloudfront.net/eyJidWNrZXQiOiAia2FybGV0LWRldi1tZWRpYSIsICJrZXkiOiAiOTIzNjZiOTgtODUybGlua2VkaW4ucG5nIiwgImVkaXRzIjoge319"
                        width="30px" height="30px" />
                    </a>

                    <a href="https://twitter.com/LINHFISH6" style="color: #fff; font-size: larger">
                    <img
                        src="https://d1a2wccegmvxly.cloudfront.net/eyJidWNrZXQiOiAia2FybGV0LWRldi1tZWRpYSIsICJrZXkiOiAiNDU1ZjVhZDQtZWRidHdpdHRlci5wbmciLCAiZWRpdHMiOiB7fX0="
                        width="30px" height="30px" />
                    </a>
                </td>
                </tr>
            </table>
            
            {section}

              <table style="padding-top: 30px; margin-right: auto; margin-left: auto;">
                <tr>
                <td>
                    <p style="
                        color: rgb(0, 0, 0);
                        font-size: 16px;
                        letter-spacing: 0.24px;
                    ">
                    Copyright &copy; {year}
                    <a href="https://havanlinh.tk/" target="_blank" style="
                        color: rgb(0, 0, 0);
                        text-decoration: none;
                        ">HRM</a>
                    </p>
                </td>
                </tr>
            </table>
        </body>
    """


class EmailTemplate:
    class WelcomeEmail:
        SUBJECT = "Welcome to HRM!"
        def BODY(name):
            return f"""
                        <table cellpadding="0" cellspacing="0" width="680px" style="
                            background-color: rgb(46, 46, 46);
                            padding: 44px 48px 64px 32px;
                            border-radius: 10px;
                            margin-right: auto; 
                            margin-left: auto;
                            ">
                            <tr style="margin-top: 0px; padding-top: 0px">
                            <td style="margin-top: 0px; padding-top: 0px">
                                <table id="logo" cellpadding="0" cellspacing="0" class="center"
                                style="max-width: 600px; margin-top: 0px; padding-top: 0px">
                                <tr>
                                    <td>
                                    <img width="600px" height="300px" style="margin-top: 0px; padding-top: 0px"
                                        src="https://d1a2wccegmvxly.cloudfront.net/eyJidWNrZXQiOiAia2FybGV0LWRldi1tZWRpYSIsICJrZXkiOiAiZDcyNWVlNGQtMjQxa2FybGV0LXdlbGNvbWUucG5nIiwgImVkaXRzIjoge319" />
                                    </td>
                                </tr>
                                </table>

                                <table id="content" cellpadding="0" cellspacing="0" align="center" style="
                                    border-radius: 5px;
                                    background-color: rgb(46, 46, 46);
                                    width: 600px;
                                ">
                                
                                <tr id="hello">
                                    <td colspan="3">
                                    <h1 style="
                                        color: rgb(255, 255, 255);
                                        margin-top: 42px;
                                        font-weight: 400;
                                        font-size: 32px;
                                        ">
                                        Welcome to HRM! 
                                    </h1>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                    <h3 style="
                                        color: #fff;
                                        margin-top: 0;
                                        margin-bottom: 32px;
                                        font-weight: bold;
                                        font-size: 18px;
                                        letter-spacing: -0.36px;
                                        ">
                                        Hello {name}, Welcome to the HRM community, we're excited to
                                        have you with us!
                                    </h3>
                                    <p style="color: #fff; margin-bottom: 32px; font-size: 16px;">
                                        Now that you're all set up, let's get you networking! 
                                    </p>
                                    
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                    <a style="color: white;background-color: #c11428; border-radius: 22px;font-size: 16px;
                                        padding: 12px 41px; text-decoration: none; " href="#" target="_blank">Go to my profile</a>
                                    </td>
                                </tr>
                                
                                <tr>
                                    <td colspan="2">
                                    <p style="margin: 0; margin-top: 32px; font-size: 16px; color: #fff">
                                        But your card can do so much more!
                                    </p>
                                    <p style="margin: 0; font-size: 16px; color: #fff">
                                        Visit havanlinh.tk to see HRM's full features.
                                    </p>
                                    </td>
                                </tr>
                                
                                <tr id="thanks">
                                    <td colspan="2">
                                    <p style="font-size: 16px;color: #fff; margin-top: 32px;">HRM Team.</p>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                    """


    class DayOffYearEmail:
        SUBJECT = "The user has been created day off year"
        def BODY(name, link):
            return f"""
                        <table cellpadding="0" cellspacing="0" width="680px" style="
                            background-color: rgb(46, 46, 46);
                            padding: 44px 48px 64px 32px;
                            border-radius: 10px;
                            margin-right: auto; 
                            margin-left: auto;
                            ">
                            <tr style="margin-top: 0px; padding-top: 0px">
                            <td style="margin-top: 0px; padding-top: 0px">
                                <table id="logo" cellpadding="0" cellspacing="0" class="center"
                                style="max-width: 600px; margin-top: 0px; padding-top: 0px">
                                <tr>
                                    <td>
                                    <img width="600px" height="300px" style="margin-top: 0px; padding-top: 0px"
                                        src="https://d1a2wccegmvxly.cloudfront.net/eyJidWNrZXQiOiAia2FybGV0LWRldi1tZWRpYSIsICJrZXkiOiAiZDcyNWVlNGQtMjQxa2FybGV0LXdlbGNvbWUucG5nIiwgImVkaXRzIjoge319" />
                                    </td>
                                </tr>
                                </table>

                                <table id="content" cellpadding="0" cellspacing="0" align="center" style="
                                    border-radius: 5px;
                                    background-color: rgb(46, 46, 46);
                                    width: 600px;
                                ">
                                
                                <tr id="hello">
                                    <td colspan="3">
                                    <h1 style="
                                        color: rgb(255, 255, 255);
                                        margin-top: 42px;
                                        font-weight: 400;
                                        font-size: 32px;
                                        ">
                                        Welcome to HRM! 
                                    </h1>
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                    <h3 style="
                                        color: #fff;
                                        margin-top: 0;
                                        margin-bottom: 32px;
                                        font-weight: bold;
                                        font-size: 18px;
                                        letter-spacing: -0.36px;
                                        ">
                                        Hello {name}, The user has been created day off year
                                    </h3>
                                   
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                    <a style="color: white;background-color: #c11428; border-radius: 22px;font-size: 16px;
                                        padding: 12px 41px; text-decoration: none; " href="{link}" target="_blank">Go to my profile</a>
                                    </td>
                                </tr>
                                
                                <tr>
                                    <td colspan="2">
                                    <p style="margin: 0; margin-top: 32px; font-size: 16px; color: #fff">
                                        But your card can do so much more!
                                    </p>
                                    <p style="margin: 0; font-size: 16px; color: #fff">
                                        Visit havanlinh.tk to see HRM's full features.
                                    </p>
                                    </td>
                                </tr>
                                
                                <tr id="thanks">
                                    <td colspan="2">
                                    <p style="font-size: 16px;color: #fff; margin-top: 32px;">HRM Team.</p>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                    """
    