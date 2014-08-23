(function($) {
    $.fn.prepFixedHeader = function () {
        return this.each( function() {
            $(this).wrap('<div class="row fixed-table"><div class="table-content"></div></div>');
        });
    };
 
    $.fn.fixedHeader = function () {
        return this.each( function() {
            var o = $(this),
            nhead = o.closest('.fixed-table'),
            $head = $('thead.header', o);
            $(document.createElement('table'))
            .addClass(o.attr('class')+' table-copy').removeClass('table-fixed-header')
            .appendTo(nhead)
            .html($head.clone().removeClass('header').addClass('header-copy header-fixed'));
            var ww = [];
            o.find('thead.header > tr:first > th').each(function (i, h){
                ww.push($(h).width());
            });
            $.each(ww, function (i, w){
                nhead.find('thead.header > tr > th:eq('+i+'), thead.header-copy > tr > th:eq('+i+')').css({width: w});
            });
             
            nhead.find('thead.header-copy').css({ margin:'0 auto',
            width: o.width()});
        });
    };
     
})(jQuery);
