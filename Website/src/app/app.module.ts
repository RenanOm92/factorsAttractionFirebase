import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule }   from '@angular/forms';

import { AngularFireModule } from '@angular/fire';
import { AngularFirestoreModule } from '@angular/fire/firestore';
import { environment } from '../environments/environment';

import { AppComponent } from './app.component';
import { HomescreenComponent } from './homescreen/homescreen.component';
import { XclickComponent } from './xclick/xclick.component';
import { StartExperimentComponent } from './start-experiment/start-experiment.component';
import { EndComponent } from './end/end.component';
import { DataService } from './data.service';
import { FillUpComponent } from './fill-up/fill-up.component';
import { InstructionsComponent } from './instructions/instructions.component';

const appRoutes: Routes = [
  { path: 'homescreen', component: HomescreenComponent },
  { path: 'instructions', component: InstructionsComponent },
  { path: 'start', component: StartExperimentComponent },
  { path: 'fillup', component: FillUpComponent },
  { path: 'xclick', component: XclickComponent },
  { path: 'end', component: EndComponent },

];


@NgModule({
  declarations: [
    AppComponent,
    HomescreenComponent,
    XclickComponent,
    StartExperimentComponent,
    EndComponent,
    FillUpComponent,
    InstructionsComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AngularFireModule.initializeApp(environment.firebase),
    AngularFirestoreModule,
	RouterModule.forRoot(
      appRoutes,
      { enableTracing: true } // <-- debugging purposes only
	  )
  ],
  providers: [DataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
