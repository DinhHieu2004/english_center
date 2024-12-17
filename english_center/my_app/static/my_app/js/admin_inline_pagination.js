(function($) {
    $(document).ready(function() {
        const rowsPerPage = 10;

        $(".inline-related").each(function() {
            var $inline = $(this);
            var $table = $inline.find("table");
            var $rows = $table.find('tbody tr');
            var totalRows = $rows.length;
            var totalPages = Math.ceil(totalRows / rowsPerPage);
            var $pagination = $("<div class='pagination'></div>");
            for (var i = 1; i <= totalPages; i++) {
                $pagination.append('<a href="#" data-page="' + i + '">' + i + '</a>');
            }
            $inline.append($pagination);
            function showPage(page) {
                var offset = (page - 1) * rowsPerPage;
                $rows.hide();
                $rows.slice(offset, offset + rowsPerPage).show(); 
                $pagination.find("a").removeClass("active");
                $pagination.find("a[data-page='" + page + "']").addClass("active");
            }
            $pagination.find("a").on("click", function(e) {
                e.preventDefault();
                var page = $(this).data("page");
                showPage(page);
            });
            showPage(1);
        });
    });
})(window.jQuery);
