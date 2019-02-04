import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from "../data.service";

@Component({
  selector: 'app-fill-up',
  templateUrl: './fill-up.component.html',
  styleUrls: ['./fill-up.component.css']
})
export class FillUpComponent implements OnInit {

  constructor(private router: Router, private dataService: DataService) { }

  showSpiral = false;
  showClickHereButtonBottomleft = false;
  showClickHereButtonTopRight = false;

  ngOnInit() {
  	this.conditionDecider(); // Check which condition should be shown
  }

  conditionDecider(){
		var condition = this.dataService.getCondition();

		if (condition == "Spiral"){
			this.showSpiral = true;
		}

		if (condition == "ClickHereBottomLeft"){
			this.showClickHereButtonBottomleft = true;
		}else if (condition == "ClickHereTopRight"){
      this.showClickHereButtonTopRight = true;
    }else {
			setTimeout(() => {
	       		this.router.navigate(['xclick']);
			}, 500);  //0.5s		
		}
	}

  btnClick() {  			
  		this.router.navigateByUrl('/xclick');
  };

}
