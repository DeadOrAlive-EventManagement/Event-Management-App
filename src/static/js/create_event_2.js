
angular.module('getData',[]).controller('ctrl',['$http','$scope',function($http,$scope){
    self = this;
    // self.obj={eventType:"",numPeople:"",eventDate:"",eventBudget:"",Venue:"",Decor:"",Caterer:""}
    self.eventType="";
    self.numPeople="";
    self.eventDate="";
    self.eventDescription="";
    self.eventBudget=0;
    self.venueDetails={venueId:"",venuePrice:"",venueVendorId:""};
    self.decorDetails={decorId:"",decorPrice:"",decorVendorId:""};
    self.catererDetails={catererId:"",catererPrice:"",catererVendorId:""};
    $scope.decors = [];
    $scope.venues = [];
    $scope.caterers = [];


    $scope.getVenue = function ()    {
        self.eventBudget = angular.element('#budget').val();
        self.numPeople = angular.element('#num_people').val();
        self.eventType = angular.element('#event_type').val();
        self.eventDate = angular.element('#datepicker').val();


        // console.log(obj.eventBudget);


        data = JSON.stringify({'value':self.eventBudget});
        alert(self.eventBudget);
        $http(
            {
                method: "POST",
                url: "/getvenue",
                data: data,
                headers: {
                    'Content-type': 'application/json'
                }
            }
        ).then(function(result){
            //here we have to display
            console.log( result.data);
            // console.log( result.data[])

            val = result.data;
            for (key in val)
            {
                console.log(val[key]["service_id"]);
                val[key]["service_id"] = val[key]["service_id"].toString();


                val[key]["vendor_id"] = val[key]["vendor_id"].toString();
                val[key]["radio_value"] = (val[key]["service_id"]+" "+val[key]["vendor_id"]+" "+val[key]["price"]+"").toString();
                alert(val[key]["radio_value"]);
            }

            $scope.venues = val;
            for (i in self.venues)
            {
                console.log(i);
            }

            // alert(result);
        } , function(error){console.log(error);});
    }
    $scope.getValTA = function()
    {
        self.eventDescription = angular.element('#description').val();
        console.log(self.eventDescription);
    }
    $scope.getDecorator = function ()    {

        ven_dets = $('input[name=venue]:checked').val();
        ven_dets = ven_dets.split(" ");
        self.venueDetails['venueId']= Number(ven_dets[0]);
        self.venueDetails['venueVendorId']= Number(ven_dets[1]);
        self.venueDetails["venuePrice"]=Number(ven_dets[2]);

        // self.budget = angular.element('#budget').val()
        data = JSON.stringify({'value':self.eventBudget});
        alert(self.eventBudget);
        $http(
            {
                method: "POST",
                url: "/getdecorator",
                data: data,
                headers: {
                    'Content-type': 'application/json'
                }
            }
        ).then(function(result){
            //here we have to display
            console.log( result.data);

            val = result.data;
            for (key in val)
            {
                val[key]["service_id"] = val[key]["service_id"].toString();
                val[key]["vendor_id"] = val[key]["vendor_id"].toString();
                val[key]["radio_value"] = (val[key]["service_id"]+" "+val[key]["vendor_id"]+" "+val[key]["price"]+"").toString();
                alert(val[key]["radio_value"]);
            }
            $scope.decors = val;
            for (i in self.decors)
            {
                console.log(i);
            }

            // alert(result);
        } , function(error){console.log(error);});
    }
    $scope.getCaterer = function ()    {
        dec_dets = $('input[name=venue]:checked').val();
        dec_dets = dec_dets.split(" ");
        self.decorDetails['decorId']= Number(dec_dets[0]);
        self.venueDetails['decorVendorId']= Number(dec_dets[1]);
        self.decorDetails["decorPrice"]=Number(dec_dets[2]);
        // self.budget = angular.element('#budget').val()
        data = JSON.stringify({'value':self.eventBudget});
        alert(self.eventBudget);
        $http(
            {
                method: "POST",
                url: "/getcaterer",
                data: data,
                headers: {
                    'Content-type': 'application/json'
                }
            }
        ).then(function(result){
            //here we have to display
            console.log(result.data);

            val = result.data;
            for (key in val)
            {
                val[key]["service_id"] = val[key]["service_id"].toString();
                val[key]["vendor_id"] = val[key]["vendor_id"].toString();
                val[key]["radio_value"] = (val[key]["service_id"]+" "+val[key]["vendor_id"]+" "+val[key]["price"]+"").toString();
                alert(val[key]["radio_value"]);
            }
            $scope.caterers = val;
            for (i in self.caterers)
            {
                console.log(i);
            }

            // alert(result);
        } , function(error){console.log(error);});
    }
    $scope.setCaterer = function()
    {
        cat_dets = $('input[name=caterer]:checked').val();
        cat_dets = cat_dets.split(" ");
        self.catererDetails['catererId']= Number(cat_dets[0]);
        self.venueDetails['catererVendorId']= Number(cat_dets[1]);
        self.catererDetails["catererPrice"]=Number(cat_dets[2]);
    }
    $scope.sendToServer = function()
    {


        obj = {"eventType":self.eventType,"numPeople": Number(self.numPeople),
        "eventDate" :self.eventDate,
        "eventBudget":self.eventBudget,
        "eventDescription":self.eventDescription,
        "venueDetails":self.venueDetails,
        "decorDetails":self.decorDetails,
        "catererDetails": self.catererDetails
    }
        console.log("in the sendtoserver function");
        console.log(obj);
        data = JSON.stringify(obj);
        // alert(self.eventBudget);
        $http(
            {
                method: "POST",
                url: "/eventcreate",
                data: data,
                headers: {
                    'Content-type': 'application/json'
                }
            }).then(function(result){
                //here we have to display
                console.log(result.data);

                val = result.data;
                if( val =="true")
                {
                    console.log("in the server");
                }


                // alert(result);
            } , function(error){console.log(error);});

    }


}])
