#aici realizam update pentru view-uri (incrementam valoarea view-ului pentru fiecare post)

from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin


#request-ul il folosim pt a face request pentru obiectul 
# la care vrem sa ii dam update la numarul de view
def update_views(request, object):
    context = {}
    
    #aici stocam modelul acelui obiect
    hit_count = get_hitcount_model().objects.get_for_object(object)
    
    #aici primim numarul de view-uri
    hits = hit_count.hits
    
    #cele doua se refera la hitcount mixing views , pt a da
    #update view-urilor acelui obiect
    hitcontext = context["hitcount"] = {"pk": hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    #aici verificam un nou user cu un ip nou , daca a vizitat pagina noastra
    if hit_count_response.hit_counted:
        #incrementare de view-uri cu 1
        hits = hits+1
        hitcontext["hitcounted"] = hit_count_response.hit_counted
        hitcontext["hit_message"] = hit_count_response.hit_message
        hitcontext["total_hits"] = hits

