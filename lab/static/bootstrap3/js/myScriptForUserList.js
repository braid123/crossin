function downloadFile(fileName, content){
	// 文档下载函数
    var aLink = document.createElement('a');
    var blob = new Blob([content]);
    var evt = document.createEvent("HTMLEvents");
    evt.initEvent("click", false, false); //initEvent 不加后两个参数在FF下会报错
    aLink.download = fileName;
    aLink.href = URL.createObjectURL(blob);
    aLink.dispatchEvent(evt);
}

function dumpdata(){
	document.getElementById('formDowload').onsubmit = function(e){
		e.preventDefault();
		var f = e.target,
			formData = new FormData(f),
			xhr = new XMLHttpRequest();
		xhr.open('POST', f.action, true);
		xhr.onreadystatechange = function(){
			if(xhr.readyState == 4 && xhr.status == 200){
				var rowNew = xhr.responseText;
				downloadFile('labuser.csv', rowNew);
			};
		};
		xhr.send(formData);
	};
};

function hidSwith(){
// 标签显示与隐藏
	var tags = document.getElementsByClassName("hidSwith");
	for(var i=0;i<tags.length;i++){
		var classVal = tags[i].getAttribute("class");
		if(classVal.match('hidden')){
			classVal = classVal.replace('hidden', 'unhid');
		}else{
			classVal = classVal.replace('unhid', 'hidden');
		};
		tags[i].setAttribute("class", classVal);
	};
};

function rename(){
	// 重命名
	var btnModOver = document.getElementById('btnModOver'),
		btnUserAdd = document.getElementById('btnUserAdd'),
		btnUserDel = document.getElementById('btnUserDel'),
		btnModify = document.getElementById('btnModify'),
		attrModify = btnModify.getAttribute('class'),
		attrModOver = btnModOver.getAttribute('class');
	attrModify += ' hidden';
	attrModOver = attrModOver.replace('hidden', '');
	btnModify.setAttribute('class', attrModify);
	btnModOver.setAttribute('class', attrModOver);
	btnUserAdd.setAttribute('disabled', true);
	btnUserDel.setAttribute('disabled', true);
	hidSwith();
};

function renameOver(){
	// 重命名完毕
	var xhr = new XMLHttpRequest(),
		para = document.getElementById('userList');
	xhr.open('GET', '?refresh=1', true);
	xhr.onreadystatechange=function(){
		if(xhr.readyState == 4 && xhr.status == 200){
			var btnModOver = document.getElementById('btnModOver'),
				btnUserAdd = document.getElementById('btnUserAdd'),
				btnUserDel = document.getElementById('btnUserDel'),
				btnModify = document.getElementById('btnModify'),
				attrModify = btnModify.getAttribute('class'),
				attrModOver = btnModOver.getAttribute('class');
			attrModOver += ' hidden';
			attrModify = attrModify.replace('hidden', '');
			btnModify.setAttribute('class', attrModify);
			btnModOver.setAttribute('class', attrModOver);
			btnUserAdd.removeAttribute('disabled');
			btnUserDel.removeAttribute('disabled');
			para.innerHTML = xhr.responseText;
			//hidSwith();
		};
	};
	xhr.send();
};

function userDel(){
    //点击用户列表-删除成员
 	var tbHid = document.getElementsByClassName('tbHid'),
		btnDelSure = document.getElementById('btnDelSure'),
		btnUserAdd = document.getElementById('btnUserAdd'),
		btnUserDel = document.getElementById('btnUserDel'),
		btnModify = document.getElementById('btnModify'),
		attrDelSure = btnDelSure.getAttribute('class'),
		attrUserDel = btnUserDel.getAttribute('class');	
	// 展示出删除的勾选框	
	for(var i=0;i<tbHid.length;i++){
		tbHid[i].setAttribute('class', 'tbHid col-lg-1');
	};
	attrDelSure = attrDelSure.replace('hidden', '');
	attrUserDel += ' hidden';
	btnUserDel.setAttribute('class', attrUserDel);
	btnDelSure.setAttribute('class', attrDelSure);
	btnUserAdd.setAttribute('disabled', true);
	btnModify.setAttribute('disabled', true);
};

function delSure(){
	// form 确认删除成员
	document.getElementById("formUserDel").onsubmit = function(e){
		e.preventDefault();
		var f = e.target,
			formData = new FormData(f),
			xhr = new XMLHttpRequest(),
			btnDelSure = document.getElementById('btnDelSure'),
			btnUserAdd = document.getElementById('btnUserAdd'),
			btnModify = document.getElementById('btnModify'),
			btnUserDel = document.getElementById('btnUserDel'),
			attrDelSure = btnDelSure.getAttribute('class'),
			attrUserDel = btnUserDel.getAttribute('class'),
			para = document.getElementById('userList');
		xhr.open("POST", f.action, true);
		xhr.onreadystatechange=function(){
			if(xhr.readyState == 4 && xhr.status == 200){
				var rowNew = xhr.responseText;
				para.innerHTML = rowNew;
				document.getElementsByClassName('tbHid')[0].setAttribute('class', 'tbHid hidden col-lg-1');
				attrDelSure += ' hidden';
				attrUserDel = attrUserDel.replace('hidden', '');
				btnUserDel.setAttribute('class', attrUserDel);
				btnDelSure.setAttribute('class', attrDelSure);
				btnUserAdd.removeAttribute('disabled');
				btnModify.removeAttribute('disabled');
			};
		};
		xhr.send(formData);
	};
};

function newAttrAdd(e, tagId){
	// 新增用户名|微信
	//document.getElementById('addNickname').setAttribute('readonly', true);
	document.getElementById('addNickname').setAttribute('value', e.parentElement.parentElement.getElementsByClassName('username')[0].innerText);
	//document.getElementById('addUsername').setAttribute('disabled', true);
	document.getElementById('addUsername').setAttribute('value', e.parentElement.parentElement.getElementsByClassName('nickname')[0].innerText);
	//document.getElementById('addWechat').setAttribute('disabled', true);
	document.getElementById('addWechat').setAttribute('value', e.parentElement.parentElement.getElementsByClassName('wechat')[0].innerText);
	
	document.getElementById('divAddUsername').setAttribute('class', 'form-group');
	document.getElementById(tagId).removeAttribute('disabled');
	document.getElementById(tagId).removeAttribute('value');
	document.getElementById(tagId).setAttribute('required', true);
	document.getElementById('update').setAttribute('value', e.parentElement.parentElement.id);
	document.getElementById('update').removeAttribute('disabled');
	$('#userAddModal').modal('show');
};

$('#userAddModal').on('hidden.bs.modal', function (e) {
	// 重置模态框数据及格式
	document.getElementById('formUserAdd').reset();
	document.getElementById('addNickname').setAttribute('readonly', true);
	document.getElementById('addUsername').setAttribute('disabled', true);
	document.getElementById('addWechat').setAttribute('disabled', true);
	document.getElementById('update').setAttribute('disabled', true);
	document.getElementById('divAddUsername').setAttribute('class', 'form-group hidden');
	//document.getElementById('addNickname').removeAttribute('readonly');
	//document.getElementById('addWechat').removeAttribute('disabled');
	
});

function userAddSure(){
	// 添加确认
	// <!-- if(document.getElementById('divAddUsername').getAttribute('class')=='form-group'){ -->
	// 	<!-- document.getElementById("formUserAdd").onsubmit = ''; -->
	// <!-- }else{ -->
	document.getElementById("formUserAdd").onsubmit = function(e){
		e.preventDefault();
		var f = e.target,
			formData = new FormData(f),
			xhr = new XMLHttpRequest();
		if(document.getElementById('divAddUsername').getAttribute('class')=='form-group'){
			para = document.getElementById(document.getElementById('update').value);
		}else{
			para = document.getElementById('userList').insertRow(0);
		};
		$('#userAddModal').modal('hide');
		xhr.open("POST", f.action, true);
		xhr.onreadystatechange=function(){
			if(xhr.readyState == 4 && xhr.status == 200){
				var rowNew = xhr.responseText;
				if(rowNew){
					para.innerHTML = rowNew;
					console.log('rowNew:'+ rowNew);
					console.log('user' + para.getElementsByTagName('input')[0].value);
					para.setAttribute('id', 'user' + para.getElementsByTagName('input')[0].value)
				}else{
					alert('本站名重复');
				};
			};
		};
		xhr.send(formData);
	};
};

function userAdd(){
	// 添加成员 清除 modal 数据
	// document.getElementById('formUserAdd').reset();
	document.getElementById('addNickname').removeAttribute('value');
	document.getElementById('addWechat').removeAttribute('value');
	document.getElementById('addWechat').removeAttribute('disabled');
	document.getElementById('addNickname').removeAttribute('readonly');
};

function inputThis(e){
	// 得到焦点，开启输入框
	// alert('1111' + name);
	// alert(e.innerText);
	// alert(e.className);
	var para = e.parentElement,
		name = e.className,
		value = e.innerText,
		uid = e.parentElement.parentElement.id.replace('user', '');
	para.innerHTML = '<input class="form-control" placeholder="' +value+ '" onblur="inputThisSure(this,' + uid + ',\'' +name+ '\')">';
	para.children[0].focus();
};

function inputThisSure(e, uid, name){
	// 失去焦点，输入确认
	// alert('222' + name);
	// alert(e.placeholder);
	var value = e.placeholder,
		info = e.value.replace(/^\s+|\s+$/g,"");
	if(info){					// 后台判断是否为空 TODO
		var xhr = new XMLHttpRequest();
		xhr.open("GET", "?"+name+"="+info+"&uid="+uid, true);
		xhr.onreadystatechange=function(){
			if(xhr.readyState == 4 && xhr.status == 200){
				if(xhr.responseText){
					alert('本站名重复');
					e.select();
				}else{
				e.parentElement.innerHTML = '<a href="#zz" class="' + name + '" style="color:red" onclick="inputThis(this)">' +info+ '</a>';
				};
			};
		};
		xhr.send();
	}else{
		e.parentElement.innerHTML = '<a href="#zz" class="' + name + '" style="color:red" onclick="inputThis(this)">' +value+ '</a>';
	};
};