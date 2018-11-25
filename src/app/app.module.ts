import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

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

const appRoutes: Routes = [
  { path: 'homescreen', component: HomescreenComponent },
  { path: 'xclick', component: XclickComponent },
  { path: 'start', component: StartExperimentComponent },
  { path: 'end', component: EndComponent },
  { path: 'fillup', component: FillUpComponent },
];


@NgModule({
  declarations: [
    AppComponent,
    HomescreenComponent,
    XclickComponent,
    StartExperimentComponent,
    EndComponent,
    FillUpComponent,
  ],
  imports: [
    BrowserModule,
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
