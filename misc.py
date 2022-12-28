

actual_par = 'appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-2162196,-1257786&emp=1&lang=ru&locale=ru&page=2&pricemarginCoeff=1.0&query=Крем для загрубевшей кожи для ног&reg=1&regions=76,80,64,83,4,38,33,70,82,69,68,86,75,30,40,48,1,22,66,31,71&resultset=catalog&sort=popular&spp=30&sppFixGeo=4&suppressSpellcheck=false'
param_is_in_issue = {k: v for k, v in map(lambda s: s.split('='), actual_par.split('&'))}


create_line_query = lambda q: f"{q.nm};{q.query} /del_{q.id}"
