//
//  ProfileViewController.swift
//  bikeshare
//
//  Created by houlianglv on 5/5/16.
//  Copyright © 2016 team O. All rights reserved.
//

import UIKit

class ProfileViewController: UIViewController {

    @IBOutlet weak var usernameLabel: UILabel!
     
    
    @IBOutlet weak var firstNameText: UITextField!
    
    @IBOutlet weak var lastNameText: UITextField!
    
    
    @IBOutlet weak var emailText: UITextField!

    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    override func viewWillAppear(animated: Bool) {
        
        
        let request = NSMutableURLRequest(URL: NSURL(string: serverDomain + "/getProfile")!)
        request.HTTPMethod = "GET"
        let session = NSURLSession.sharedSession()
        
        let task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
            print("Response: \(response)")
            let strData = NSString(data: (data)!, encoding: NSUTF8StringEncoding)!
            
            print("Body: \(strData)")
            
            do {
                
                let json = try NSJSONSerialization.JSONObjectWithData(data!, options: []) as! [String: AnyObject]
                let resMessage = json["status"] as? String
                print("status: \(resMessage)" )
                    
                
            } catch {
                print("error>>>>>>>>>>>>>>")
                print("error serializing JSON: \(error)")
            }
            
            if let httpResponse = response as? NSHTTPURLResponse {
                if(httpResponse.statusCode == 200){
                    //sign up successfully
                    //all ui change must happen in main thread. I think the issue is that async http request is in different thread.
                    //so use this method to push code back to main thread
                    print("response success")
                }
            } else {
                assertionFailure("unexpected response")
            }
            
        self.usernameLabel.text = "test name"
        self.firstNameText.text = "test text"
            
            
        })
        task.resume()
        
        
    }
    
    
    @IBAction func BasicInfoSaveBtn(sender: AnyObject) {
        let firstName = firstNameText.text
        let lastName = lastNameText.text
        let email = emailText.text
        
    }
    
    @IBAction func logoutBtn(sender: AnyObject) {
        let appDomain = NSBundle.mainBundle().bundleIdentifier
        NSUserDefaults.standardUserDefaults().removePersistentDomainForName(appDomain!)
        self.navigationController?.popViewControllerAnimated(true)
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
