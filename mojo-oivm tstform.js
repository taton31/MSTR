submitUpdates:function e(Bu,B0,Br){
	Bu=Bj(Bu)
	if(mstrApp.isVI&&!mstrApp.isDossier&&this.model.controller.isDatasetPanelRefreshAction(Bu))
	{
		B0=p.wrapMethods(this.model.getDatasetsUpdateCallback(),B0)
	}
	this.cleanFormatLayoutXML(Bu)
	var Bq={actions:Bu},Bl,Bo,Bx,Bn=false
	BT.forEach(Bu,function Bt(B2)
	{
		if(B2.disablePU){
			Bn=true
			delete B2.disablePU
		}
		BT.forEach(B2.actions,Bt)
		return !Bn
	})
	if(!Bn)
	{
		var Bm=mstrmojo.rw.model.RetrievalKeysConfig.getConsolidatedConfig(Bu),Bz=mstrmojo.rw.model.UpdateKeysConfig.getConsolidatedConfig(Bu)
		if(!Ah.isEmpty(Bm))
		{
			Bq.partialRetrieval=Bm
		}
		if(!Ah.isEmpty(Bz))
		{
			Bq.partialUpdate=Bz
		}
	}
	if(Br)
	{
		Bl=Br.style
		Bo=Br.config
		Bx=Br.params
	}
	if(!Bo)
	{
		Bo={showProgress:true,hideProgress:true,progressStateText:a}
	}
	if(!Bl)
	{
		Bq.style=this.defaultStyle
	}
	else
	{
		var B1=Bq.style=Ah.clone(this.defaultStyle)
		AY(Bl.params,B1.params)
	}
	Bq.style.name=(Bl&&Bl.name)||mstrApp.styleName
	var Bs=	{
		taskId:"mojoRWManipulation",
		rwb:this.rwb,
		messageID:this.msgId,
		stateID:-1,
		params:JSON.stringify(Bq)
		}
	Bx=BQ.call(this,Bx)
	AY(Bx,Bs)
	Bo.preserveUndo=(Br&&Br.noUpdate)||false
	Bo.preserveStid=(Br&&Br.preserveStid)||false
	var Bw=this,By=true,
	Bp=p.override(
	{
		success:function(B2,B3){
			if(B2.status===2){
				By=false
				Bw.submitUpdates([],B0,Br)
			}
			else
			{
				By=true
				return this._super(B2,B3)
			}
		},
		complete:function(){
			if(this._super&&By)
			{
				this._super()
			}
		}
	},
	AY(B0))
	if(!(Br&&Br.hideCancel))
	{
		Bo.waitBoxCfg=Ah.copy({showCancel:true},Bo.waitBoxCfg)
	}
	if(Br&&Br.message)
	{
		Bo.waitBoxCfg=Ah.copy({message:Br.message},Bo.waitBoxCfg)
	}
	var Bv=mstrApp.isAppStatePause&&mstrApp.isAppStatePause()
	if(Br&&Br.resolveOnly!==undefined)
	{
		Bs.resolveOnly=Br.resolveOnly
	}
	else
	{
		if(Bv)
		{
			Bs.resolveOnly=true
		}
	}
	if(Br&&Br.excludeData!==undefined)
	{
		Bs.excludeData=Br.excludeData
	}
	else
	{
		if(Bv)
		{
			Bs.excludeData=true
		}
	}
	if(Br&&Br.noDeltaXML!==undefined)
	{
		Bs.noDeltaXML=Br.noDeltaXML
	}
	if(Bs.resolveOnly&&Bs.excludeData)
	{	
		mstrApp.enableUpdate=true
	}
	Ao.call(this,Bs,Bp,Bo)
	}