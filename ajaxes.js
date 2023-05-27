function freightstartloading794642() {
    //$("#loaderIcon").show();
    $('#52276').attr('disabled', 'disabled').removeClass("green").addClass("grey");
    jQuery.ajax({
        url: "ajax/freight_loading.php",
        data: {f: "27210522", token: "175317188"},
        type: "GET",
        success: function (data) {
            $("#status").html(data);
            //$("#loaderIcon").hide();
            $('#52276').removeAttr('disabled').removeClass("grey").addClass("green");
        },
        error: function () {
        }
    });
}

function freightstartdriving794642() {
    //$("#loaderIcon").show();
    $('#52276').attr('disabled', 'disabled').removeClass("green").addClass("grey");
    jQuery.ajax({
        url: "ajax/freight_driving.php",
        data: {f: "27210522", token: "175317188"},
        type: "GET",
        success: function (data) {
            $("#status").html(data);
            //$("#loaderIcon").hide();
            $('#52276').removeAttr('disabled').removeClass("grey").addClass("green");
        },
        error: function () {
        }
    });
}

function freightcontinue794642() {
    //$("#loaderIcon").show();
    $('#52276').attr('disabled', 'disabled').removeClass("green").addClass("grey");
    jQuery.ajax({
        url: "ajax/freight_continue.php",
        data: {f: "27210522", token: "175317188"},
        type: "GET",
        success: function (data) {
            $("#status").html(data);
            //$("#loaderIcon").hide();
            $('#52276').removeAttr('disabled').removeClass("grey").addClass("green");
        },
        error: function () {
        }
    });
}

function freightstartunloading794642() {
    //$("#loaderIcon").show();
    $('#52276').attr('disabled', 'disabled').removeClass("green").addClass("grey");
    jQuery.ajax({
        url: "ajax/freight_unloading.php",
        data: {f: "27210522", token: "175317188"},
        type: "GET",
        success: function (data) {
            $("#status").html(data);
            //$("#loaderIcon").hide();
            $('#52276').removeAttr('disabled').removeClass("grey").addClass("green");
        },
        error: function () {
        }
    });
}

function freightstartfinishing794642() {
    //$("#loaderIcon").show();
    $('#52276').attr('disabled', 'disabled').removeClass("green").addClass("grey");
    jQuery.ajax({
        url: "ajax/freight_finish.php",
        data: {f: "27210522", token: "175317188"},
        type: "GET",
        success: function (data) {
            $("#status").html(data);
            //$("#loaderIcon").hide();
            $('#52276').removeAttr('disabled').removeClass("grey").addClass("green");
        },
        error: function () {
        }
    });
}

function freightautoall794642() {
    //$("#loaderIcon").show();
    jQuery.ajax({
        url: "ajax/freight_autoall.php",
        data: {n: "27210522", token: "175317188"},
        type: "GET",
        success: function (data) {
            $("#status").html(data);
            //$("#loaderIcon").hide();
        },
        error: function () {
        }
    });
}

function freightautowhemployee794642() {
    //$("#loaderIcon").show();
    jQuery.ajax({
        url: "ajax/freight_autowhemployee.php",
        data: {n: "27210522", token: "175317188"},
        type: "GET",
        success: function (data) {
            $("#status").html(data);
            //$("#loaderIcon").hide();
        },
        error: function () {
        }
    });
}

function freightautotrailer794642() {
    //$("#loaderIcon").show();
    jQuery.ajax({
        url: "ajax/freight_autotrailer.php",
        data: {n: "27210522", token: "175317188"},
        type: "GET",
        success: function (data) {
            $("#status").html(data);
            //$("#loaderIcon").hide();
        },
        error: function () {
        }
    });
}

function freightautotruck794642() {
    //$("#loaderIcon").show();
    jQuery.ajax({
        url: "ajax/freight_autotruck.php",
        data: {n: "27210522", token: "175317188"},
        type: "GET",
        success: function (data) {
            $("#status").html(data);
            //$("#loaderIcon").hide();
        },
        error: function () {
        }
    });
}

function freightspeedup() {
    //$("#loaderIcon").show();
    $('#speedup').attr('disabled', 'disabled').removeClass("yellow-casablanca").addClass("grey");
    jQuery.ajax({
        url: "ajax/freight_speedup.php",
        data: {f: "27210522", token: "175317188"},
        type: "GET",
        success: function (data) {
            $("#status").html(data);
            //$("#loaderIcon").hide();
            $('#speedup').removeAttr('disabled').removeClass("grey").addClass("yellow-casablanca");
        },
        error: function () {
        }
    });
}
