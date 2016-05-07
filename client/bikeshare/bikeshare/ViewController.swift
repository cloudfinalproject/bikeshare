//
//  ViewController.swift
//  bikeshare
//
//  Created by houlianglv on 4/12/16.
//  Copyright © 2016 team O. All rights reserved.
//

import UIKit
import GoogleMaps

var serverDomain = "http://localhost:5000"

class ViewController: UIViewController, UITabBarDelegate {



    @IBOutlet weak var usernameLabel: UILabel!
    @IBOutlet weak var gmsMapView: GMSMapView!
    @IBOutlet weak var tabBar: UITabBar!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        //tabBar delegate
        tabBar.delegate = self

        // Do any additional setup after loading the view, typically from a nib.
        let camera = GMSCameraPosition.cameraWithLatitude(-33.86,
            longitude: 151.20, zoom: 6)

        gmsMapView.camera = camera

        let marker = GMSMarker()
        marker.position = CLLocationCoordinate2DMake(-33.86, 151.20)
        marker.title = "Sydney"
        marker.snippet = "Australia"
        marker.map = gmsMapView

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    override func viewDidAppear(animated: Bool) {
        super.viewDidAppear(true)
        let prefs:NSUserDefaults = NSUserDefaults.standardUserDefaults()
        let isLoggedIn:Bool = prefs.boolForKey("ISLOGGEDIN") as Bool
        if (!isLoggedIn) {
            self.performSegueWithIdentifier("goto_login", sender: self)
        } else {
            self.usernameLabel.text = prefs.valueForKey("USERNAME") as? String
        }
    }

    @IBAction func logoutTapped(sender: UIButton) {
        let appDomain = NSBundle.mainBundle().bundleIdentifier
        NSUserDefaults.standardUserDefaults().removePersistentDomainForName(appDomain!)

        self.performSegueWithIdentifier("goto_login", sender: self)
    }

    func tabBar(tabBar: UITabBar, didSelectItem item: UITabBarItem) {
        let index = Int((self.tabBar.items?.indexOf(item))!)
        switch index {
        case 0:
            self.performSegueWithIdentifier("goto_dashboard", sender: self)
        case 1:
            self.performSegueWithIdentifier("goto_messages", sender: self)
        case 2:
            self.performSegueWithIdentifier("goto_bikes", sender: self)
        case 3:
            self.performSegueWithIdentifier("goto_profile", sender: self)
        default:
            return
        }

    }


}

