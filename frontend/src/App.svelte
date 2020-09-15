<script>
	import axios from 'axios';
	import { onMount } from "svelte";

	let description = '';
	let tasks = [];

	const headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json'
	}

	function createTask(description) {
		axios.post('/task', {
			description: description
		})
		.then(function (response) {
			console.log(`Task with id: ${response.data['id']} succesfully created!`);
			getTasks();
		})
		.catch(function (error) {
			console.log(error);
		})
	}

	function deleteTask(id) {
		axios.delete(`/task/${id}`)
		.then(function (response) {
			console.log(`Task with id: ${id} succesfully deleted!`);
			getTasks();
		})
		.catch(function (error) {
			console.log(error);
		});
	}

	function changeStateTask(id, state) {
		axios.patch(`/task/change/${id}?state=${state}`)
		.then(function (response) {
			console.log(`Task with id: ${id} was succesfully set to ${state}`);
			getTasks();
		})
		.catch(function (error) {
			console.log(error);
		});
	}

	function getTasks() {
		axios.get("/tasks")
		.then(function (response) {
			tasks = response.data;
		})
		.catch(function (error) {
			console.log(error);
		})
	}

	const onKeyPress = (e) => {
		if (e.charCode === 13) {
			createTask(description); 
			description = '';
		}
	};

	onMount(async function() {
		getTasks();
	});
</script>

<main>
	<h1>Svelte.js + Flask API Example</h1>
	<p>Add your to-do items, you have so much to do. Hurry up man!</p>

	<div class="wrapper">
		<input type="text" bind:value={description} on:keypress={onKeyPress} id="input-task" placeholder="Add item and press enter">
		<ul class="task-list">

			{#each tasks as task}
			<li class="complete-{task.active}">
				<label class="checkbox">
					<input type='checkbox' on:change={changeStateTask(task.id, this.checked)} bind:checked={task.active} class='status'> 
					<span></span>
				</label>				  
				{task.description}
				<button on:click={deleteTask(task.id)} class='delete'>
					<i class="fa fa-times"></i>
				</button>
			</li>
			{/each}

		</ul>
		<div class="bottom-border"></div>
	</div>
</main>

<style type="text/scss" global>
@import "../public/global.scss";	
</style>