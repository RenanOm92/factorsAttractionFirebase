import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-instructions',
  templateUrl: './instructions.component.html',
  styleUrls: ['./instructions.component.css']
})
export class InstructionsComponent {

  constructor(private router: Router) { }

  btnClick() {
        this.router.navigateByUrl('/start');
	};

}
