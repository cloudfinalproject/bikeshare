//
//  LoginViewController.swift
//  bikeshare
//
//  Created by houlianglv on 4/16/16.
//  Copyright © 2016 team O. All rights reserved.
//

import UIKit

class LoginViewController: UIViewController {


    @IBOutlet weak var usernameText: UITextField!
    @IBOutlet weak var passwordText: UITextField!

    override func viewDidLoad() {
        super.viewDidLoad()
        print("login view")

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    


    @IBAction func loginTapped(sender: UIButton) {
        //authentication code
        let username = usernameText.text
        let password = passwordText.text
        if(username == "" || password == ""){
            //Create the AlertController
            let actionSheetController: UIAlertController = UIAlertController(title: "Alert", message: "Login failed", preferredStyle: .Alert)

            //Create and add the Cancel action
            let cancelAction: UIAlertAction = UIAlertAction(title: "Cancel", style: .Cancel) { action -> Void in
                //Do some stuff
            }
            actionSheetController.addAction(cancelAction)

            //Present the AlertController
            self.presentViewController(actionSheetController, animated: true, completion: nil)

        }else{

        }

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
