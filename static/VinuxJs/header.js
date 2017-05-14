var STATIC_URL_JS = "";

//--------------------------------------------------------------------------------------
function makeHeader(tabIndex, userName) {
  // get the correct array
  var arrayLoc = [
    [ '/Vinux/cellarView/', 'Cave' ],//[ url, tab name]
    [ '/Vinux/goneBottlesView/', 'Déjà bu' ] 
    ];
  var shownName = userName[0].toUpperCase() + userName.substring(1)

  // add the banner
  var myVar = '<div class="header">'
        + '<div class="myTab myTitle">'
      + '    <p>' + shownName + ', bienvenu sur Vinux <a class="smaller" href="/accounts/logout/?next=/accounts/login/">- logout</a></p>'
      + '</div>';
  // add the tabs
  for (var tab = 0; tab < arrayLoc.length; ++tab) {
    var theUrl = arrayLoc[tab][0];
    var theTitle = arrayLoc[tab][1];
    var tmp = '<div  id="id_tab' + tab + '" class="myTab tabN' + tab + '">';
    tmp += '<a class="menu" href="' + theUrl + '">' + theTitle + '</a></div>'
    myVar += tmp;
  }
  myVar += '</div>';
  document.write(myVar);
  $('#id_tab' + tabIndex).addClass('selectedTab')
};

