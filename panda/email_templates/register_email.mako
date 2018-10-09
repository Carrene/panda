<%
    url = '%s?t_=%s' % (registeration_callback_url, registeration_token)
%>

<html lang="en">
<head>
  <meta name="viewport" content="width=device-width"/>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <title>CAS</title>
</head>

<body style="margin: 0; padding: 0">
  <table class="container" align="center" style="width: 600px; border-collapse: collapse">
    <tr>
      <td>
        <table class="header" bgcolor="#1A237E" align="center" style="height: 160px; width: 100%">
          <tr>
            <td valign="bottom" style="padding-left: 55px">
              <img src="http://nightly.cas.carrene.com/logo.png" alt="CAS" width="80px">
            </td>
          </tr>
          <tr>
            <td valign="top" style="padding-left: 50px">
              <p style="font-size: 10px; font-weight: 100; color: #FFF; margin: 0">
                <span style="font-weight: 500">A</span>uthentication <span style="font-weight: 500">S</span>ervice</p>
            </td>
          </tr>
        </table>
        <table class="body" style="background-color: #FFF; padding: 50px 50px 145px 50px; display: block; border: 1px solid #CCC">
          <tr>
            <td valign="bottom">
              <p style="font-size: 30px; font-weight: bold; color: #1A237E; margin: 0">Hi dear
                <span style="color: #2196F3">CAS</span> user,
              </p>
            </td>
          </tr>
          <tr>
            <td>
              <p style="font-size: 20px; font-weight: 300; margin: 0; padding-top: 30px">Lorem ipsum dolor sit amet,
                  consectetur adipisicing elit. Consequ officiis! Autem commodi cum cupiditate ea
              </p>
            </td>
          </tr>
          <tr>
            <td valign="top">
              <p style="font-size: 20px; font-weight: 500; color: #1A237E; margin: 0; padding-top: 30px">Click on this
                <a href="${url}" target="_blank" style="color: #2196F3; font-size: 18px;">
                  link </a>to reset your password.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
