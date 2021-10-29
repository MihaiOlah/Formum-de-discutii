// Navigation bar display

// Sterge clasa hide ca sa putem vedea bara de navigatie
function  hideIconBar() {
    var bar_icon = document.getElementById("bar-icon");
    var navigation_bar = document.getElementById("navigation");

    bar_icon.setAttribute("style", "display:none;");
    navigation_bar.classList.remove("hide");
}

// Adauga clasa hide ca sa ascunda bara de navigatie
function showIconBar() {
    var bar_icon = document.getElementById("bar-icon");
    var navigation_bar = document.getElementById("navigation");

    bar_icon.setAttribute("style", "display:blockl");
    navigation_bar.classList.add("hide");
}

// Arata cutia de scris comentariile
function showComment() {
    var comment_area = document.getElementById("comment-area");
    comment_area.setAttribute("style", "display:block;");
}

// Arata cutia de scris replay-urile
function showReply() {
    var reply_area = document.getElementById("reply-area");
    reply_area.setAttribute("style", "display:block;");
}