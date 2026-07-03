---
layout: null
sitemap: false
---

{% assign counter = 0 %}
var documents = [{% for page in site.pages %}{% if page.url contains '.xml' or page.url contains 'assets' or page.url contains 'category' or page.url contains 'tag' %}{% else %}{
    "id": {{ counter }},
    "url": "{{ site.url }}{{site.baseurl}}{{ page.url }}",
    "title": "{{ page.title }}",
    "body": "{{ page.content | markdownify | replace: '.', '. ' | replace: '</h2>', ': ' | replace: '</h3>', ': ' | replace: '</h4>', ': ' | replace: '</p>', ' ' | strip_html | strip_newlines | replace: '  ', ' ' | replace: '"', ' ' }}"{% assign counter = counter | plus: 1 %}
    }, {% endif %}{% endfor %}{% for page in site.without-plugin %}{
    "id": {{ counter }},
    "url": "{{ site.url }}{{site.baseurl}}{{ page.url }}",
    "title": "{{ page.title }}",
    "body": "{{ page.content | markdownify | replace: '.', '. ' | replace: '</h2>', ': ' | replace: '</h3>', ': ' | replace: '</h4>', ': ' | replace: '</p>', ' ' | strip_html | strip_newlines | replace: '  ', ' ' | replace: '"', ' ' }}"{% assign counter = counter | plus: 1 %}
    }, {% endfor %}{% for page in site.posts %}{
    "id": {{ counter }},
    "url": "{{ site.url }}{{site.baseurl}}{{ page.url }}",
    "title": "{{ page.title }}",
    "body": "{{ page.date | date: "%Y/%m/%d" }} - {{ page.content | markdownify | replace: '.', '. ' | replace: '</h2>', ': ' | replace: '</h3>', ': ' | replace: '</h4>', ': ' | replace: '</p>', ' ' | strip_html | strip_newlines | replace: '  ', ' ' | replace: '"', ' ' }}"{% assign counter = counter | plus: 1 %}
    }{% if forloop.last %}{% else %}, {% endif %}{% endfor %}];

var idx = lunr(function () {
    this.ref('id')
    this.field('title')
    this.field('body')

    documents.forEach(function (doc) {
        this.add(doc)
    }, this)
});
function escapeHtml(text) {
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function highlightTerm(text, term) {
    var safeText = escapeHtml(text);
    if (!term) {
        return safeText;
    }

    term.trim().split(/\s+/).filter(Boolean).forEach(function (word) {
        var pattern = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        var regex = new RegExp('(' + pattern + ')', 'gi');
        safeText = safeText.replace(regex, '<mark class="search-highlight">$1</mark>');
    });

    return safeText;
}

function parseSearchBody(rawBody) {
    var match = rawBody.match(/^(\d{4}\/\d{2}\/\d{2})\s*-\s*(.*)$/);
    if (match) {
        return { date: match[1], excerpt: match[2] };
    }
    return { date: null, excerpt: rawBody };
}

function closeSearchModal() {
    $('#lunrsearchresults').hide(200);
    $('body').removeClass('modal-open');
}

function lunr_search(term) {
    term = (term || '').trim();
    if (!term) {
        return false;
    }

    var container = document.getElementById('lunrsearchresults');
    if (container.parentElement !== document.body) {
        document.body.appendChild(container);
    }

    $('#lunrsearchresults').show(200);
    $('body').addClass('modal-open');

    container.innerHTML =
        '<div id="resultsmodal" class="modal fade show d-block search-results-modal" tabindex="-1" role="dialog" aria-labelledby="modtit" aria-modal="true">' +
            '<div class="modal-dialog modal-dialog-scrollable search-results-dialog shadow" role="document">' +
                '<div class="modal-content">' +
                    '<div class="modal-header search-results-header">' +
                        '<div class="search-results-heading">' +
                            '<h5 class="modal-title" id="modtit"></h5>' +
                            '<p class="search-results-count" id="modcount"></p>' +
                        '</div>' +
                        '<button type="button" class="search-results-close" id="btnx-top" aria-label="Închide">&times;</button>' +
                    '</div>' +
                    '<div class="modal-body search-results-body">' +
                        '<ul class="search-results-list mb-0"></ul>' +
                    '</div>' +
                    '<div class="modal-footer search-results-footer">' +
                        '<button type="button" class="btn btn-primary btn-sm" id="btnx">Închide</button>' +
                    '</div>' +
                '</div>' +
            '</div>' +
        '</div>';

    var results = idx.search(term);
    var listEl = document.querySelector('#lunrsearchresults .search-results-list');
    document.getElementById('modtit').textContent = 'Rezultate pentru „' + term + '”';

    if (results.length > 0) {
        document.getElementById('modcount').textContent =
            results.length + (results.length === 1 ? ' articol găsit' : ' articole găsite');

        for (var i = 0; i < results.length; i++) {
            var doc = documents[results[i].ref];
            var parsed = parseSearchBody(doc.body);
            var excerpt = parsed.excerpt.substring(0, 160);
            if (parsed.excerpt.length > 160) {
                excerpt += '…';
            }

            var itemHtml =
                '<li class="lunrsearchresult">' +
                    '<a href="' + doc.url + '" class="search-link">' +
                        '<span class="title">' + highlightTerm(doc.title, term) + '</span>';

            if (parsed.date) {
                itemHtml += '<span class="search-date">' + parsed.date + '</span>';
            }

            itemHtml +=
                        '<span class="body">' + highlightTerm(excerpt, term) + '</span>' +
                    '</a>' +
                '</li>';

            listEl.innerHTML += itemHtml;
        }
    } else {
        document.getElementById('modcount').textContent = '';
        listEl.innerHTML =
            '<li class="lunrsearchresult search-results-empty">' +
                '<p class="search-results-empty-title">Niciun rezultat</p>' +
                '<p class="search-results-empty-text">Nu am găsit nimic pentru „' + escapeHtml(term) + '”. Încearcă alt nume de destinație.</p>' +
            '</li>';
    }

    return false;
}

$(function () {
    $('#lunrsearchresults').on('click', '#btnx, #btnx-top', closeSearchModal);

    $('#lunrsearchresults').on('click', '#resultsmodal', function (e) {
        if (!$(e.target).closest('.modal-dialog').length) {
            closeSearchModal();
        }
    });

    $(document).on('keyup.searchModal', function (e) {
        if (e.keyCode === 27 && $('#lunrsearchresults').is(':visible')) {
            closeSearchModal();
        }
    });
});