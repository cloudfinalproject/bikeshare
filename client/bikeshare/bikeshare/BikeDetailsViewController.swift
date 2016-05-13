//
//  BikeDetailsViewController.swift
//  bikeshare
//
//  Created by Derrick on 5/12/16.
//  Copyright © 2016 team O. All rights reserved.
//

import UIKit



class BikeDetailsViewController: UIViewController {
    
    
    @IBOutlet weak var bikeModelField: UITextField!
    @IBOutlet weak var addressField: UITextField!
    @IBOutlet weak var cityField: UITextField!
    @IBOutlet weak var stateField: UITextField!
    @IBOutlet weak var countryField: UITextField!
    @IBOutlet weak var postCodeField: UITextField!
    @IBOutlet weak var priceField: UITextField!
    @IBOutlet weak var availabilitySwitch: UISwitch!
    @IBOutlet weak var detailsFiled: UITextView!
    
    
    var currentBike : Dictionary<String, AnyObject>?
    var lat: Float?
    var lng: Float?
    
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Do any additional setup after loading the view.
        
        if (currentBike?.count != 0){
            dispatch_async(dispatch_get_main_queue(),{
                print("currentBike \(self.currentBike)")
                self.bikeModelField?.text = self.currentBike!["model"] as? String
                self.addressField?.text = self.currentBike!["address"] as? String
                self.cityField?.text = self.currentBike?["city"] as? String
                self.stateField?.text = self.currentBike?["state"] as? String
                self.countryField?.text = self.currentBike?["country"] as? String
                self.postCodeField?.text = self.currentBike?["postcode"] as? String
                self.priceField?.text = (self.currentBike!["price"] as? Float)?.description
                self.availabilitySwitch?.on = (self.currentBike!["status"] as? Bool)!
                self.detailsFiled?.text = self.currentBike!["details"] as? String

            })
        }
        
    }
    
    private func addBike(){
        
        let bikeModel = self.bikeModelField.text!
        let address =  self.addressField.text!
        let city = self.cityField.text!
        let state = self.stateField.text!
        let country = self.countryField.text!
        let postcode = self.postCodeField.text!
        let price = (self.priceField.text! as NSString).floatValue
        let availability = self.availabilitySwitch.on
        let details = self.detailsFiled.text!
        let s_lat = lat!
        let s_lng = lng!
        
        
        let request = NSMutableURLRequest(URL: NSURL(string: serverDomain + "/addBike")!)
        request.HTTPMethod = "POST"
        
        let payload = "model=\(bikeModel)&address=\(address)&city=\(city)&state=\(state)&country=\(country)&postcode=\(postcode)&price=\(price)&available=\(availability)&details=\(details)&lat=\(s_lat)&lon=\(s_lng)"
        let payloadWithoutSpace = payload.stringByAddingPercentEncodingWithAllowedCharacters(.URLHostAllowedCharacterSet())
        request.HTTPBody = payloadWithoutSpace!.dataUsingEncoding(NSUTF8StringEncoding)
        let session = NSURLSession.sharedSession()
        
        let task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
            print("Response: \(response)")
            let strData = NSString(data: (data)!, encoding: NSUTF8StringEncoding)
            print("Body: \(strData)")
            
            if let httpResponse = response as? NSHTTPURLResponse {
                if(httpResponse.statusCode == 200){
                    //sign up successfully
                    //all ui change must happen in main thread. I think the issue is that async http request is in different thread.
                    //so use this method to push code back to main thread
                    print("Saved!!!!!")
                }
            } else {
                assertionFailure("unexpected response")
            }
        })
        task.resume()
    }
    
    
    private func updateBike(){
        
        let bikeModel = self.bikeModelField.text!
        let address =  self.addressField.text!
        let city = self.cityField.text!
        let state = self.stateField.text!
        let country = self.countryField.text!
        let postcode = self.postCodeField.text!
        let price = (self.priceField.text! as NSString).floatValue
        let availability = self.availabilitySwitch.on
        let details = self.detailsFiled.text!
        let bid = self.currentBike!["bid"]!
        let s_lat = lat!
        let s_lng = lng!
        
        
        let request = NSMutableURLRequest(URL: NSURL(string: serverDomain + "/editBike/" + "\(bid)")!)
        request.HTTPMethod = "POST"
        
        let payload = "model=\(bikeModel)&address=\(address)&city=\(city)&state=\(state)&country=\(country)&postcode=\(postcode)&price=\(price)&available=\(availability)&details=\(details)&lat=\(s_lat)&lon=\(s_lng)"
        let payloadWithoutSpace = payload.stringByAddingPercentEncodingWithAllowedCharacters(.URLHostAllowedCharacterSet())
        request.HTTPBody = payloadWithoutSpace!.dataUsingEncoding(NSUTF8StringEncoding)
        let session = NSURLSession.sharedSession()
        
        let task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
            print("Response: \(response)")
            let strData = NSString(data: (data)!, encoding: NSUTF8StringEncoding)
            print("Body: \(strData)")
            
            if let httpResponse = response as? NSHTTPURLResponse {
                if(httpResponse.statusCode == 200){
                    //sign up successfully
                    //all ui change must happen in main thread. I think the issue is that async http request is in different thread.
                    //so use this method to push code back to main thread
                    print("Saved!!!!!")
                }
            } else {
                assertionFailure("unexpected response")
            }
        })
        task.resume()
    }
    
    private func get_coordinate(addressALL: String){
        
        
        let encodedAddress = addressALL.stringByAddingPercentEncodingWithAllowedCharacters(.URLHostAllowedCharacterSet())
        let request = NSMutableURLRequest(URL: NSURL(string: "http://maps.googleapis.com/maps/api/geocode/json?address=" + encodedAddress!)!)
        request.HTTPMethod = "GET"
        let session = NSURLSession.sharedSession()
        let task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
            print("Response: \(response)")
            let strData = NSString(data: (data)!, encoding: NSUTF8StringEncoding)!
            print("Body: \(strData)")
            
            if let httpResponse = response as? NSHTTPURLResponse {
                if(httpResponse.statusCode == 200){
                    print("response success")
                    let jsonData: NSData = data! /* get your json data */
                    do{
                        let jsonDict = try NSJSONSerialization.JSONObjectWithData(jsonData, options: .AllowFragments)
                        self.lat = jsonDict["results"]!![0]["geometry"]!!["location"]!!["lat"] as? Float
                        self.lng = jsonDict["results"]!![0]["geometry"]!!["location"]!!["lng"] as? Float
                        if (self.currentBike?.count == 0 ){
                            self.addBike()
                        }
                        else{
                            self.updateBike()
                        }

                        //self.usernameLabel.text = jsonDict["result"]!["user"]!!["username"] as? String
                        
                    }
                    catch{
                        print(">>>>> exception catched during geocoding")
                    }
                }
            } else {
                assertionFailure("unexpected response")
            }
            
        })
        task.resume()
        
    }
    
    @IBAction func editBike(sender: AnyObject) {
        let address =  self.addressField.text!
        let city = self.cityField.text!
        let state = self.stateField.text!
        
        get_coordinate(address + "," + city + ", " + state)

        

        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    /*
     // MARK: - Navigation
     
     // In a storyboard-based application, you will often want to do a little preparation before navigation
     override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
     // Get the new view controller using segue.destinationViewController.
     // Pass the selected object to the new view controller.
     }
     */
    
}