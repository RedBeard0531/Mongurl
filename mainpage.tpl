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

    <form action='/' method='POST'>
        <label for="url"> Add </label>
        <input type="text" name="url" />
    </form>

    <ol>
        %for url in urls:
        <li>
            <a href="/{{url['_id']}}/info" class="link_id">{{url['_id']}}</a> -
            <img width="10" height="10" src="{{urljoin(url['url'], '/favicon.ico')}}" />
            <a href="/{{url['_id']}}">{{url['url']}}</a>
            ({{url['visits']}} visits)
        </li>
        %end
    </ol>
</body>
</html>

%# vim: set ft=html:
