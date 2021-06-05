$(document).ready(function () {
    $('.sidenav > div > a[href="' + window.location.pathname + '"]').addClass('active');
    $('.sidenav > div > a[href="' + window.location.pathname + window.location.search + '"]').addClass('active');
    setTimeout(function () {
        $(".alert-dismissible").alert("close");
    }, 5000);
    table = $('#jsTable').DataTable({
        responsive: true,
        dom: '<"row no-gutters flex-nowrap"<"flex-grow-1"f><"flex-shrink-0 ml-1"l>>t<"row"<"col-sm-12 col-md-6"i><"col-sm-12 col-md-6"p>>',
        lengthMenu: [5, 10, 25, 50, 100],
        pagingType: "numbers",
        pageLength: 10,
        language: {
            lengthMenu: "_MENU_",
            search: "_INPUT_",
            searchPlaceholder: "Search"
        },
        columnDefs: [{
            targets: [-1],
            orderable: false
        },
        {
            targets: [0, -1],
            responsivePriority: 1
        }]
    });

    var rootPassword = $("#rootPassword").text();
    $("#rootPassword").text(rootPassword.replace(/./g, '*'));

    $('#ipAddressButton').click(function () {
        var $temp = $("<input>");
        $("body").append($temp);
        $temp.val($('#ipAddress').text()).select();
        document.execCommand("copy");
        $temp.remove();
    });
    $('#rootPasswordButton').click(function () {
        var $temp = $("#rootPassword");
        if ($temp.text() === rootPassword) {
            $temp.text(rootPassword.replace(/./g, '*'));
        }
        else {
            $temp.text(rootPassword);
        }
    });
    $('#consoleButton').click(function (e) {
        var $temp = $("<input>");
        $("body").append($temp);
        $temp.val(rootPassword).select();
        document.execCommand("copy");
        $temp.remove();
        if (!confirm('The root password has been copied to your clipboard.\nAfter pressing OK, you will be redirected to the Linode in-browser terminal.\nPaste the password when asked using CTRL-SHIFT-V.')) {
            e.preventDefault();
        }
    });

    $('input[name*="partner_id"]').on("click", function () {
        if (confirm("You should leave this field empty unless it's absolutely necessary to manually provide the Partner ID.\n\nAre you sure you want to continue?")) {
            $('input[name*="partner_id"]').focus()
        }
        else {
            $('input[name*="company"]').focus()
            $('input[name*="partner_id"]').val("");
        }
    });

    $('#jsTable_length').removeClass('dataTables_length');
    $('#jsTable_filter').removeClass('dataTables_filter');
    $('#jsTable_filter > label').contents().unwrap();
    $('#jsTable_length > label').contents().unwrap();
    $('#jsTable_filter > input').removeClass("form-control-sm");
    $('#jsTable_length > select').removeClass("custom-select-sm form-control-sm");

    $('input[name*="rate"]').on("input", updateItem);
    $('input[name*="hours"]').on("input", updateItem);
    $('input[name*="amount"]').on("input", updateItem);

    $('#id_items_table tbody').each(function (e) {
        $(this).children('tr').each(function (e) {
            $(this).children('td').each(function (e) {
                $(this).children('input').each(function (e) {
                    $(this).trigger("input");
                })
            })
        })
    })

    $('#invoiceForm').submit(function (e) {
        $('input[name*="items-"]:disabled').each(function (e) {
            $(this).removeAttr('disabled');
        });
    });

    $('#startButton').on("click", startTimeCounter);
    $('#stopButton').on("click", stopTimeCounter);

    var t;
    function startTimeCounter() {
        $('#startButton').addClass('d-none');
        $('#submitButton').attr('disabled', true);
        $('#stopButton').removeClass('d-none');
        $('#id_duration').attr('readonly', true);

        var startTime = Math.floor(Date.now() / 1000);

        t = setInterval(function () {
            var diff = Math.floor(Date.now() / 1000) - startTime;
            var h = formatTime(Math.floor(diff / 3600));
            var m = formatTime(Math.floor(diff % 3600 / 60));
            document.getElementById("id_duration").value = h + ":" + m;
        }, 500);
    }

    function stopTimeCounter() {
        $('#stopButton').addClass('d-none');
        $('#startButton').removeClass('d-none');
        $('#submitButton').attr('disabled', false);
        $('#id_duration').attr('readonly', false);
        clearInterval(t);
    }
});

function updateItem(e) {
    number = e.target.name.match(/\d+/);

    var hours = 'input[name="items-' + number + '-hours"]';
    var rate = 'input[name="items-' + number + '-rate"]';
    var amount = 'input[name="items-' + number + '-amount"]';


    if ($(hours).val() || $(rate).val()) {
        $(amount).prop('disabled', true);
        if ($(hours).val() && $(rate).val()) {
            $(amount).val(($(hours).val() * $(rate).val()).toFixed(2)).trigger('change');
        }
        else {
            $(amount).val("").trigger('change');
        }
    }
    else if ($(amount).val()) {
        $(rate).prop('disabled', true);
        $(hours).prop('disabled', true);
    }
    else {
        $(rate).prop('disabled', false);
        $(hours).prop('disabled', false);
        $(amount).prop('disabled', false);
    }
}

function toggleSidebar() {
    $('.sidenav').toggleClass("sidenav-show");
    $('.main').toggleClass("main-below");
    $('body').toggleClass("body-below");
    $('.sidenav-button').toggleClass("sidenav-button-show");
}

function formatTime(i) {
    if (i < 10) { i = "0" + i };  // add zero in front of numbers < 10
    return i;
}
