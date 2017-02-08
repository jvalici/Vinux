//--------------------------------------------------------------------------------------
//cf:https://docs.djangoproject.com/en/1.2/ref/contrib/csrf/
//the following bit of cod is a copy past from: http://stackoverflow.com/questions/5407463/how-to-use-post-with-django
if (!$)
    $ = django.jQuery;
//--------------------------------------------------------------------------------------
//get the cookie by name
function getCookie(name) 
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '') 
    {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) 
        {
            var cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) 
            {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

//--------------------------------------------------------------------------------------
// modify the send request to include the cookie    
$('html').ajaxSend(
    function(event, xhr, settings)
    {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) 
        {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
);
//end of copy past from: http://stackoverflow.com/questions/5407463/how-to-use-post-with-django

