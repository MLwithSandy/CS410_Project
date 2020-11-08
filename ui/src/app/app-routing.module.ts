import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {RouterModule, Routes} from '@angular/router';
import {HomeComponent} from './home/home.component';
import {P404Component} from './p404/p404.component';
import {CustomPreloadingService} from './services/custom-preloading.service';

const appRoutes: Routes = [
  {path: 'home', component: HomeComponent},
  {path: '', redirectTo: '/home', pathMatch: 'full'},
  {path: '**', component: P404Component}
];


@NgModule({
  declarations: [],
  imports: [
    RouterModule.forRoot(appRoutes, {preloadingStrategy: CustomPreloadingService}),
    CommonModule
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
