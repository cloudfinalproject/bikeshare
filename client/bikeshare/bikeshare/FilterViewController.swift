//
//  FilterViewController.swift
//  bikeshare
//
//  Created by houlianglv on 5/11/16.
//  Copyright © 2016 team O. All rights reserved.
//

import UIKit

class FilterViewController: UIViewController {

    //outlets
    @IBOutlet weak var fromDatePicker: UIDatePicker!
    @IBOutlet weak var toDatePicker: UIDatePicker!
    @IBOutlet weak var fromDateLabel: UILabel!
    @IBOutlet weak var toDateLabel: UILabel!

    var fromDate:NSDate = NSDate()
    var toDate:NSDate = NSDate().dateByAddingTimeInterval(21600)

    var onDataAvailable : ((data: String) -> ())?

    //send data back to main view
    func sendData(data: String) {
        self.onDataAvailable?(data: data)
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }

    override func viewWillAppear(animated: Bool) {
        let dateFormatter = NSDateFormatter()
        dateFormatter.dateFormat = "dd-MM-yyyy HH:mm"
        var strDate = dateFormatter.stringFromDate(fromDate)
        self.fromDateLabel.text = strDate
        self.fromDatePicker.date = fromDate
        strDate = dateFormatter.stringFromDate(toDate)
        self.toDateLabel.text = strDate
        self.toDatePicker.date = toDate

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


    //actions
    @IBAction func onCancelTapped(sender: UIBarButtonItem) {
        self.dismissViewControllerAnimated(true, completion: nil)
    }

    @IBAction func onConfirmTapped(sender: UIButton) {
        //build the parameter and send to the main view
        self.sendData(fromDateLabel.text! + "*" + toDateLabel.text!)
        self.dismissViewControllerAnimated(true, completion: nil)
    }

    @IBAction func onFromDateValueChanged(sender: UIDatePicker) {
        if fromDatePicker.date.compare(toDatePicker.date) == NSComparisonResult.OrderedDescending {
            showAlert()
            fromDatePicker.date = fromDate
            return
        }
        let dateFormatter = NSDateFormatter()
        dateFormatter.dateFormat = "dd-MM-yyyy HH:mm"
        let strDate = dateFormatter.stringFromDate(fromDatePicker.date)
        self.fromDate = fromDatePicker.date
        self.fromDateLabel.text = strDate
    }

    @IBAction func onToDateValueChanged(sender: UIDatePicker) {
        if fromDatePicker.date.compare(toDatePicker.date) == NSComparisonResult.OrderedDescending {
            showAlert()
            toDatePicker.date = toDate
            return
        }
        let dateFormatter = NSDateFormatter()
        dateFormatter.dateFormat = "dd-MM-yyyy HH:mm"
        let strDate = dateFormatter.stringFromDate(toDatePicker.date)
        self.toDate = toDatePicker.date
        self.toDateLabel.text = strDate
    }

    func showAlert(){
        //Create the AlertController
        let actionSheetController: UIAlertController = UIAlertController(title: "Alert", message: "End Date cannot be earlier than From Date", preferredStyle: .Alert)
        //Create and add the Cancel action
        let cancelAction: UIAlertAction = UIAlertAction(title: "OK", style: .Cancel) { action -> Void in }
        actionSheetController.addAction(cancelAction)
        //Present the AlertController
        self.presentViewController(actionSheetController, animated: true, completion: nil)
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
