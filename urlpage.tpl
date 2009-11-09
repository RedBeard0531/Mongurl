<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> 
<html> 
<head> 
  <title>Mongurl - A URL shortner using MongoDB</title> 
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" > 
  <style>
      .link_id {
          font-family: monospace;
          font-style: bold;
      }
  </style>
</head> 
<body>
    <h1>Mongurl</h1>

    <h2>{{_id}}</h2>

    <div>
    <img src="{{urljoin(url, '/favicon.ico')}}" />
    </div>

    <p>
    URL: <a href="/{{_id}}">{{url}}</a><br />
    Clicks: {{visits}}<br />
    Created: {{created.ctime()}}<br />
    Last Clicked: {{last_visited}}<br />

    <p>
    For all links with this url:<br />
    First linked to: {{real_url['created'].ctime()}}<br />
    Clicks: {{real_url['visits']}}<br />
    Last Clicked: {{real_url['last_visited']}}<br />

    %if len(real_url['shorts']) > 1:
    <p>
    Other mongurls:
    <ul>
        %for id in real_url['shorts']:
        %if id != _id:
            <li>
            <a href="/{{id}}/info" class="link_id">{{id}}</a>
            </li>
        %end
        %end
    </ul>
    %end


</body>
</html>

%# vim: set ft=html:
