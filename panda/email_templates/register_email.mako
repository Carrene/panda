<%
    url = '%s?t_=%s' % (registration_callback_url, registration_token)
%>

<html lang="en">
<head>
  <meta name="viewport" content="width=device-width"/>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <title>Maestro</title>
</head>

<body style="margin: 0; padding: 0">
  <table class="container" align="center" style="width: 600px; border-collapse: collapse">
    <tr>
      <td>
        <table class="header" bgcolor="#463B5B" align="center" style="height: 160px; width: 100%">
          <tr>
            <td valign="center" style="padding-left: 35px">
              <img src="http://nightly.cas.carrene.com/maestro-light.png" alt="maestro" width="55px">
            </td>
          </tr>
        </table>
        <table class="body" style="background-color: #FFF; padding: 50px 50px 145px 50px; display: block; border: 1px solid #EEE">
          <tr>
            <td valign="bottom">
              <p style="font-size: 30px; font-weight: bold; color: #232323; margin: 0">Hi dear
                <span style="color: #463B5B">Maestro</span> user,
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
              <p style="font-size: 20px; font-weight: 500; color: #232323; margin: 0; padding-top: 30px">Click on this
                <a href="${url}" target="_blank" style="color: #463B5B; font-size: 18px;">
                  link </a>to create your account.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
