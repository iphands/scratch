use std::alloc::System;

#[global_allocator]
static A: System = System;

fn main() {
    let home = std::env::var("HOME");

    match std::env::var("PWD") {
        Ok(full_path) => {
            let path = match home {
                Ok(h) => full_path.replace(&h, "~"),
                _ => full_path
            };

            if path.len() < 25 {
                print!("{}", path);
                return;
            }

            let mut output = String::new();
            let mut chars = path.chars();

            let limit = path.split("/").collect::<Vec<&str>>().len() - 2;

            if limit < 2 {
                print!("{}", path);
                return;
            }

            let mut count = 0;

            loop {
                // println!("{} {}", count, limit);

                match chars.next() {
                    Some(c) => {
                        if count < limit {
                            if c == '~' {
                                output.push(c);
                                continue;
                            }

                            if c == '/' {
                                output.push(c);
                                output.push(chars.next().unwrap());
                                count += 1;
                                continue;
                            }
                            continue;
                        }

                        output.push(c);
                    },
                    None => break
                }
            }
            print!("{}", output);
            // println!("{}", path)
        }
        _ => {
            print!("error")
        }
    }
}
