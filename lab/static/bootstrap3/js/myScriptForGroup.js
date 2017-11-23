function allCheck(node1){
	var node=document.getElementsByName("studentgroup");
	for (var x = 0; x < node.length; x++) {
		node[x].checked=node1.checked;
	}
};
/*
当所有的状态都选中全选自动选上
*/
function chose(node){
	var flag=true;//用于遍历是否是全部变量设置
	var allM=document.getElementsByName("all")[0];
	var node=document.getElementsByName("studentgroup");
	for (var x = 0; x < node.length; x++) {
		if(node[x].checked==false){//只要有一个没选中，就退出遍历，标记设置为false
			flag=false;
			break;
		}
	}
	if(flag){
		allM.checked=true;
	}else{
		allM.checked=false;
	}
};

function ResetGroupName(){
	$("#addGroupname").val("");
	$("#addGroupNote").val("");
	$("#delGroupId").val("");
};

function AddGroupName(){
	// 添加确认
	// 群名不可重复
	document.getElementById("formGroupAdd").onsubmit = function(e){
		e.preventDefault();
		var f = e.target,
			formData = new FormData(f),
			xhr = new XMLHttpRequest(),
			elem_li_a = document.createElement('a'),
			elem_li = document.createElement('li'); // 生成一个button元素
		elem_li.setAttribute("role","presentation");//设置元素属性	
		elem_li.setAttribute("class","nav active ");
		elem_li_a.setAttribute('href', "/group/student?group=");
		console.log('elem_li_a', elem_li_a);
		console.log('elem_li',elem_li);
		// <a href='{% url "group:studentgroup"%}?group={{ group.id }}'>
		document.querySelector('#row-left > ul').append(elem_li); // 添加到UL中去
		elem_li.appendChild(elem_li_a);
		console.log('elem_li_a', elem_li_a);
		console.log('elem_li',elem_li);
		$('#GroupAddModal').modal('hide');
		xhr.open("POST", f.action, true);
		xhr.onreadystatechange=function(){
			console.log('xhr', xhr);
			if(xhr.readyState == 4 && xhr.status == 200){
				var rowNew = xhr.responseText;
				if(rowNew){
					console.log('elem_li', elem_li);
                    console.log('rowNew', rowNew);
					elem_li_a.innerHTML = rowNew;
					console.log('elem_li.innerHTML', elem_li_a.innerHTML)
				}else{
					alert('本群名重复');
				};
			};
		};
		xhr.send(formData);
	};
};

function DelGroupId(){
	// 删除群ID
	console.log('Enter DelGroupId');
	document.getElementById("formGroupDel").onsubmit = function(e){
		e.preventDefault();
		var f = e.target,
			formData = new FormData(f),
			xhr = new XMLHttpRequest(),
			para = document.getElementById('delGroupId');
		console.log(para.val);
		xhr.open("POST", f.action, true);
		xhr.onreadystatechange=function(){
			if(xhr.readyState == 4 && xhr.status == 200){
				var rowNew = xhr.responseText;
				console.log('rowNew');
				para.innerHTML = rowNew;
			};
		};
		xhr.send(formData);
	};
	console.log('Exited DelGroupId');
};

function ChangeUserGroup(){
	console.log('Enter the ChangeUserGroup');
    // iGroupFlag = $("#AllUserInGroup").is(":checked");
	// if(iGroupFlag === true){
    // 	unCheckedBoxs = $("input[type=checkbox]").not("input:checked").length;
	// 	CheckedBoxs =  $('input[type=checkbox]:checked').length - 1;
	// }
	// else if(iGroupFlag === false){
	//    //未勾选个数
    // 	unCheckedBoxs = $("input[type=checkbox]").not("input:checked").length - 1;
	//     // 勾选个数
	// 	CheckedBoxs = $('input[type=checkbox]:checked').length;
	// }
	// 新的群组ID
	// NewGroupId = $('select option:selected').val();
    // OneGroupBox = $('input[type=checkbox]').length - 1;
	// for(var i=0;i<OneGroupBox;i++){
	// 	OldGroupId = $('input[name=studentgroup]')[i].value;
	// 	if(NewGroupId != OldGroupId)
	// 	   OldGroupId = NewGroupId;
	// };
    console.log('Exited the ChangeUserGroup');
};